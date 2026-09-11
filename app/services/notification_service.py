from datetime import datetime


def send_notification(
    notification_type: str,
    message: str,
):
    """
    Simulates sending a notification.

    This can later be replaced with:
    - Email
    - SMS
    - Push Notification
    """

    print(
        f"[{datetime.now()}] "
        f"{notification_type}: "
        f"{message}"
    )


def notify_order_placed(
    order_id: int,
):
    send_notification(
        notification_type="ORDER PLACED",
        message=(
            f"Order #{order_id} "
            f"has been placed successfully."
        ),
    )


def notify_order_status_changed(
    order_id: int,
    order_status: str,
):
    status_messages = {
        "Accepted": "Your order has been accepted.",
        "Preparing": "Your food is being prepared.",
        "Ready": "Your food is ready.",
        "Picked Up": (
            "Your order has been picked up "
            "by the delivery partner."
        ),
        "Out for Delivery": (
            "Your order is out for delivery."
        ),
        "Delivered": (
            "Your order has been delivered."
        ),
    }

    message = status_messages.get(
        order_status,
        f"Your order status is now {order_status}.",
    )

    send_notification(
        notification_type="ORDER STATUS",
        message=(
            f"Order #{order_id}: "
            f"{message}"
        ),
    )


def notify_driver_assigned(
    order_id: int,
    driver_name: str,
):
    send_notification(
        notification_type="DRIVER ASSIGNED",
        message=(
            f"Order #{order_id} has been assigned "
            f"to delivery partner {driver_name}."
        ),
    )


def notify_payment_success(
    order_id: int,
):
    send_notification(
        notification_type="PAYMENT SUCCESS",
        message=(
            f"Payment for Order #{order_id} "
            f"was successful."
        ),
    )


def notify_refund_processed(
    order_id: int,
    refund_amount: float,
):
    send_notification(
        notification_type="REFUND PROCESSED",
        message=(
            f"Refund of {refund_amount} "
            f"for Order #{order_id} "
            f"has been processed."
        ),
    )