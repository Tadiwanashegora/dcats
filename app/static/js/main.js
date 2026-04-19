/* ── DCATS main.js ────────────────────────────────────────────────────────── */

// Auto-dismiss alerts after 5 seconds
document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = "opacity 0.5s";
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  // Mark all / Mark none buttons on record attendance page
  const markAllBtn  = document.getElementById("mark-all-present");
  const markNoneBtn = document.getElementById("mark-all-absent");

  if (markAllBtn) {
    markAllBtn.addEventListener("click", () => {
      document.querySelectorAll("input[value='present']").forEach(r => r.checked = true);
    });
  }
  if (markNoneBtn) {
    markNoneBtn.addEventListener("click", () => {
      document.querySelectorAll("input[value='absent']").forEach(r => r.checked = true);
    });
  }

  // Highlight rows where status = absent
  document.querySelectorAll(".data-table tbody tr").forEach(row => {
    const badge = row.querySelector(".badge-danger");
    if (badge && badge.textContent.trim().toLowerCase() === "absent") {
      row.style.background = "#fff5f5";
    }
  });
});
