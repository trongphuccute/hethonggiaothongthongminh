document.getElementById('loginForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const email = document.getElementById('loginEmail').value.trim();
  const password = document.getElementById('loginPassword').value.trim();

  if (email === "" || password === "") {
    alert("⚠️ Vui lòng nhập đầy đủ thông tin!");
    return;
  }

  // Mô phỏng xác thực (sau này có thể thay bằng backend API)
  if (email === "user@example.com" && password === "123456") {
    alert("✅ Đăng nhập thành công!");
    window.location.href = "index.html";
  } else {
    alert("❌ Sai email hoặc mật khẩu!");
  }
});
