export default function BookingsPage() {
  async function loadBookings() {
    const response = await fetch(
      "/api/bookings"
    );

    return response.json();
  }

  async function createBooking() {
    const response = await fetch(
      "/api/bookings",
      {
        method: "POST",
        body: JSON.stringify({
          hotelId: "123",
          date: "2026-09-20"
        })
      }
    );

    return response.json();
  }

  return (
    <div>
      Bookings
    </div>
  );
}