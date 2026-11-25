(() => {
  const cfg = window.MONITORLAB || {};
  const intervalMs = Math.max(5, Number(cfg.refreshSeconds) || 7) * 1000;
  const statusEl = document.getElementById("refresh-status");
  const manualBtn = document.getElementById("manual-refresh");

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text;
  }

  function updateDashboard(items) {
    const list = document.getElementById("server-list");
    if (!list) return;
    items.forEach((item) => {
      const row = list.querySelector(`[data-server-id="${item.server.id}"]`);
      if (!row) return;
      const m = item.metrics;
      const status = row.querySelector('[data-field="status"]');
      const cpu = row.querySelector('[data-field="cpu"]');
      const mem = row.querySelector('[data-field="mem"]');
      if (status) {
        status.textContent = m.status;
        status.className = `badge badge-${String(m.status).toLowerCase()}`;
      }
      if (cpu) cpu.textContent = `CPU ${m.cpu_percent}%`;
      if (mem) mem.textContent = `Mem ${m.memory.percent}%`;
    });
  }

  function updateDetail(payload) {
    const root = document.getElementById("detail-metrics");
    if (!root || !payload.metrics) return;
    const m = payload.metrics;
    const status = document.getElementById("detail-status");
    if (status) {
      status.textContent = m.status;
      status.className = `badge badge-${String(m.status).toLowerCase()}`;
    }
    const cpu = root.querySelector('[data-field="cpu"]');
    const mem = root.querySelector('[data-field="mem"]');
    const net = root.querySelector('[data-field="net"]');
    const ports = root.querySelector('[data-field="ports"]');
    if (cpu) cpu.textContent = `${m.cpu_percent}%`;
    if (mem) {
      mem.textContent = `${m.memory.used_gb} / ${m.memory.total_gb} GB (${m.memory.percent}%)`;
    }
    if (net) {
      net.textContent = `↓ ${m.network.in_mbps} Mbps · ↑ ${m.network.out_mbps} Mbps`;
    }
    if (ports) ports.textContent = (m.open_ports || []).join(", ");
  }

  async function refresh() {
    if (!cfg.metricsUrl) return;
    try {
      const response = await fetch(cfg.metricsUrl, {
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      });
      if (response.status === 401) {
        window.location.href = "/login";
        return;
      }
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (cfg.mode === "detail") updateDetail(data);
      else updateDashboard(data.items || []);
      setStatus(`Updated ${new Date().toLocaleTimeString()}`);
    } catch (_err) {
      setStatus("Refresh failed — will retry");
    }
  }

  if (manualBtn) {
    manualBtn.addEventListener("click", () => {
      setStatus("Refreshing…");
      refresh();
    });
  }

  if (cfg.metricsUrl) {
    setInterval(refresh, intervalMs);
  }
})();
