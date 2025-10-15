import { useState } from "react";
import axiosInstance from "../utils/axiosInstance";
import Link from "next/link"; // For client-side navigation in Next.js
import "../styles/SignUp.css"; 

export default function SignUp() {
  const [form, setForm] = useState({ user_name: "", user_email: "", password: "" });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axiosInstance.post("/signup", form);
      alert("Signup successful!");
    } catch (error) {
      console.error(error);
      alert("Signup failed!");
    }
  };

  return (
    <div className="container">
      {/* Left side illustration */}
     

      {/* Right side form */}
      <div className="form-container">
        <div className="highlighted-card">
          <form onSubmit={handleSubmit}>
            <h2>Sign Up</h2>

            <input
              type="text"
              placeholder="Full Name"
              value={form.user_name}
              onChange={(e) => setForm({ ...form, user_name: e.target.value })}
            />

            <input
              type="email"
              placeholder="Email"
              value={form.user_email}
              onChange={(e) => setForm({ ...form, user_email: e.target.value })}
            />

            <input
              type="password"
              placeholder="Password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />

            <button type="submit">Sign Up</button>

            <p>
              Already have an account? <Link href="/signin">Login</Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
