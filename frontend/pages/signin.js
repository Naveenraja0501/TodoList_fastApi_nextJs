import { useState } from "react";
import { useRouter } from "next/navigation";
import axiosInstance from "../utils/axiosInstance";
import { useUserStore } from "../store/userStore";
import Link from "next/link";
import "../styles/SignIn.css"; 

export default function SignIn() {
  const [form, setForm] = useState({ user_email: "", password: "" });
  const setUser = useUserStore((state) => state.setUser);
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axiosInstance.post("/login", form);
      setUser(res.data);
      localStorage.setItem("user", JSON.stringify(res.data));
      alert("Login successful!");
      router.push("/");
    } catch (err) {
      console.error(err);
      alert("Login failed! Check your credentials.");
    }
  };

  return (
    <div className="container">


      {/* Right side form */}
      <div className="form-container">
        <div className="highlighted-card">
          <form onSubmit={handleSubmit}>
            <h2>Sign In</h2>

            <input
              type="email"
              placeholder="Email"
              required
              value={form.user_email}
              onChange={(e) => setForm({ ...form, user_email: e.target.value })}
            />

            <input
              type="password"
              placeholder="Password"
              required
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />

            <button type="submit">Sign In</button>

            <p>
              Don't have an account? <Link href="/signup">Sign Up</Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
