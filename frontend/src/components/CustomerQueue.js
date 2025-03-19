import React, { useState, useEffect } from "react";
import axios from "axios";

const CustomerQueue = ({ customers }) => {
  const [queue, setQueue] = useState([]); // ✅ Ensure it starts as an empty array
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/customers")
      .then((response) => {
        setQueue(response.data.customers || []); // ✅ Fallback to an empty array
        setLoading(false);
      })
      .catch((error) => {
        console.error("❌ Error fetching customers:", error);
        setQueue([]); // ✅ Prevent undefined error
        setLoading(false);
      });
  }, [customers]); // ✅ Re-fetch when `customers` prop updates

  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-2">Customer Queue</h2>

      {/* ✅ Wrapping the queue list inside a scrollable container */}
      <div className="max-h-60 overflow-y-auto border border-gray-300 p-2 rounded-lg">
        {loading ? (
          <p>Loading...</p>
        ) : queue.length === 0 ? (
          <p>No customers in queue.</p>
        ) : (
          <ul>
            {queue.map((customer, index) => (
              <li key={index} className="border p-2 my-1 bg-gray-100 rounded-md">
                {customer.priority} - {customer.service_time}s
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default CustomerQueue;
