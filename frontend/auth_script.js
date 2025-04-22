const BASE_URL = "http://localhost:8000"; // Update this if your backend runs elsewhere

// Handle Signup
async function handleSignup() {
  const email = document.getElementById("signup-email").value;
  const password = document.getElementById("signup-password").value;
  const confirm = document.getElementById("signup-confirm").value;

  if (!email || !password || !confirm) {
    alert("Please fill in all fields");
    return;
  }

  if (password !== confirm) {
    alert("Passwords do not match");
    return;
  }

  const res = await fetch(`${BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();

  if (data.success) {
    alert(data.message || "Signup successful. You can now login.");
    document.getElementById("check").checked = false; // switch to login tab
  } else {
    alert(data.detail || "Signup failed.");
  }
}

// Handle Login
async function handleLogin() {
  console.log(document.getElementById("login-email").value); // should not be null
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  if (!email || !password) {
    alert("Please enter both email and password.");
    return;
  }

  console.log(email, password)

  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  console.log(res)
  const data = await res.json();
  console.log(data)
  if (data.success && data.data.access_token) {
    alert("Login successful!");
    localStorage.setItem("token", data.data.access_token);
    localStorage.setItem("user_id", data.data.user_id);
    // redirect to dashboard
    window.location.href = "index.html";

  } else {
    alert(data.detail || "Login failed.");
  }
}
