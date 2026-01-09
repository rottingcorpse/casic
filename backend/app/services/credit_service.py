from __future__ import annotations

from typing import Any, cast

from sqlalchemy.orm import Session as DBSession

from ..models.db import CasinoBalanceAdjustment, ChipPurchase, Seat, Session, Table, User


class CreditService:
    """Service for managing player credit operations."""

    @staticmethod
    def get_credit_purchases_for_seat(
        db: DBSession,
        session_id: str,
        seat_no: int,
    ) -> list[ChipPurchase]:
        """
        Get all credit purchases for a specific seat in a session.
        
        Args:
            db: Database session
            session_id: Session ID
            seat_no: Seat number
            
        Returns:
            List of credit purchases for the seat
        """
        return (
            db.query(ChipPurchase)
            .filter(
                ChipPurchase.session_id == session_id,
                ChipPurchase.seat_no == seat_no,
                ChipPurchase.payment_type == "credit",
                ChipPurchase.amount > 0,
            )
            .all()
        )

    @staticmethod
    def calculate_total_credit(credit_purchases: list[ChipPurchase]) -> int:
        """
        Calculate total credit from a list of credit purchases.
        
        Args:
            credit_purchases: List of credit purchases
            
        Returns:
            Total credit amount
        """
        return sum(int(cast(int, cp.amount)) for cp in credit_purchases)

    @staticmethod
    def create_balance_adjustment(
        db: DBSession,
        amount: int,
        comment: str,
        created_by_user_id: int,
    ) -> CasinoBalanceAdjustment:
        """
        Create a casino balance adjustment.
        
        Args:
            db: Database session
            amount: Adjustment amount (positive for profit, negative for expense)
            comment: Description of the adjustment
            created_by_user_id: ID of the user creating the adjustment
            
        Returns:
            Created adjustment record
        """
        adjustment = CasinoBalanceAdjustment(
            amount=amount,
            comment=comment.strip(),
            created_by_user_id=created_by_user_id,
        )
        db.add(adjustment)
        db.flush()
        return adjustment

    @staticmethod
    def close_credit(
        db: DBSession,
        session: Session,
        seat: Seat,
        amount_to_close: int,
        user: User,
    ) -> None:
        """
        Close credit for a player by creating a balance adjustment and removing credit purchases.
        
        This method:
        1. Creates a balance adjustment for the credit amount
        2. Removes or reduces credit purchases to match the amount to close
        
        Args:
            db: Database session
            session: Session object
            seat: Seat object
            amount_to_close: Amount of credit to close
            user: User performing the operation
        """
        # Get credit purchases for this seat
        credit_purchases = CreditService.get_credit_purchases_for_seat(
            db, cast(str, session.id), int(cast(int, seat.seat_no))
        )
        
        # Get player name and session info for comment
        player_name = seat.player_name if seat.player_name else f"Seat {seat.seat_no}"
        
        table = db.query(Table).filter(Table.id == session.table_id).first()
        table_name = table.name if table else "Unknown"
        
        session_date = session.date.strftime("%d.%m.%Y") if session.date else ""
        
        # Create balance adjustment (positive amount = profit for casino)
        adjustment = CreditService.create_balance_adjustment(
            db,
            amount=amount_to_close,
            comment=f"Долг ({player_name}) - {table_name} - {session_date}",
            created_by_user_id=int(cast(int, user.id)),
        )
        
        # Remove credit purchases by deleting them
        # We need to delete enough credit purchases to match the amount
        remaining_to_close = amount_to_close
        for cp in sorted(credit_purchases, key=lambda x: x.created_at):
            if remaining_to_close <= 0:
                break
            
            cp_amount = int(cast(int, cp.amount))
            if cp_amount <= remaining_to_close:
                # Delete the entire purchase
                db.delete(cp)
                remaining_to_close -= cp_amount
            else:
                # Partially close by reducing the amount
                cp.amount = cast(Any, cp_amount - remaining_to_close)
                remaining_to_close = 0

    @staticmethod
    def close_credit_for_session(
        db: DBSession,
        session: Session,
        seat: Seat,
        user: User,
    ) -> int:
        """
        Close all credit for a seat when closing a session.
        
        This is used during session closing to automatically close all player credits.
        
        Args:
            db: Database session
            session: Session object
            seat: Seat object
            user: User performing the operation
            
        Returns:
            Amount of credit that was closed
        """
        # Get credit purchases for this seat
        credit_purchases = CreditService.get_credit_purchases_for_seat(
            db, cast(str, session.id), int(cast(int, seat.seat_no))
        )
        
        total_credit = CreditService.calculate_total_credit(credit_purchases)
        
        if total_credit == 0:
            return 0
        
        # Close all credit
        CreditService.close_credit(db, session, seat, total_credit, user)
        
        return total_credit
