// Public sector pay — apples-to-apples comparison across 13 large U.S. cities.
const fmt$ = n => (n == null) ? "—" : "$" + Math.round(n).toLocaleString();
const fmtYrs = n => (n == null) ? "—" : (n + " yr" + (n === 1 ? "" : "s"));

// ROLE_LABELS used to be hard-coded; now derived from data.role_definitions at init time.
let ROLE_LABELS = {
  police_officer: "Police: patrol officer (rank-and-file)",
  firefighter: "Fire: firefighter (rank-and-file)",
  sanitation_worker: "Sanitation worker (city-employed)",
  transit_bus_operator: "Transit bus operator (regional authority)",
};
let ROLE_REGISTRY = null;  // populated from data.role_definitions

const SOURCE_TAGS = {
  cba: { cls: "cba", text: "CBA" },
  city_pay_plan_schedule: { cls: "cba", text: "City pay plan" },
  city_classification_page: { cls: "cba", text: "City class spec" },
  city_personnel_class_spec: { cls: "cba", text: "City class spec" },
  city_salary_schedule: { cls: "cba", text: "City salary schedule" },
  city_pay_plan: { cls: "cba", text: "City pay plan" },
  city_salary_range_report: { cls: "cba", text: "City salary report" },
  official_salary_schedule: { cls: "cba", text: "Official schedule" },
  cba_with_dept_page: { cls: "cba", text: "CBA / dept page" },
  department_careers_page: { cls: "dept", text: "Dept careers page" },
  department_pay_scales_page: { cls: "dept", text: "Dept pay scale" },
  department_pay_scale_pdf: { cls: "dept", text: "Dept pay scale" },
  union_wage_chart: { cls: "dept", text: "Union wage chart" },
  union_wage_page: { cls: "dept", text: "Union wage page" },
  agency_announcement: { cls: "dept", text: "Agency announcement" },
  agency_employment_page: { cls: "dept", text: "Agency page" },
  press_release_with_meet_confer: { cls: "dept", text: "Press release / agreement" },
  salary_aggregator: { cls: "gap", text: "Aggregator (verify)" },
  private_contractor: { cls: "private", text: "Private contractor" },
  needs_research: { cls: "gap", text: "Gap" },
};

let DATA;
let state = { role: "police_officer", metric: "top_base", city: null, nycCol: false, nycAllIn: false };

(async function init() {
  DATA = await fetch("data.json").then(r => r.json());

  // Build role registry from data, fall back to defaults if missing
  if (DATA.role_definitions) {
    ROLE_REGISTRY = DATA.role_definitions;
    ROLE_LABELS = {};
    for (const [k, v] of Object.entries(ROLE_REGISTRY)) ROLE_LABELS[k] = v.label;
  }

  // Compute per-role verified-cell counts so we can hide empty roles + show coverage in the label
  const roleCoverage = {};
  for (const k of Object.keys(ROLE_REGISTRY || ROLE_LABELS)) {
    let n = 0;
    for (const c of DATA.cities) {
      const r = c.roles[k];
      if (r && r.top_base != null) n++;
    }
    roleCoverage[k] = n;
  }

  // Build role dropdown grouped by category — only show roles with at least 1 verified cell
  const roleSel = document.getElementById("role-pick");
  if (ROLE_REGISTRY) {
    const categories = {};
    for (const [k, v] of Object.entries(ROLE_REGISTRY)) {
      if (roleCoverage[k] === 0) continue;  // hide empty roles
      (categories[v.category] = categories[v.category] || []).push([k, v]);
    }
    const catOrder = ["Police", "Fire", "Sanitation", "Transit", "Education", "Other public sector"];
    for (const cat of catOrder) {
      if (!categories[cat]) continue;
      const og = document.createElement("optgroup"); og.label = cat;
      categories[cat].sort((a, b) => a[1].rank_order - b[1].rank_order);
      for (const [k, v] of categories[cat]) {
        const o = document.createElement("option");
        o.value = k;
        o.textContent = `${v.label} (${roleCoverage[k]}/${DATA.cities.length})`;
        og.appendChild(o);
      }
      roleSel.appendChild(og);
    }
  } else {
    for (const [k, v] of Object.entries(ROLE_LABELS)) {
      if (roleCoverage[k] === 0) continue;
      const o = document.createElement("option"); o.value = k;
      o.textContent = `${v} (${roleCoverage[k]}/${DATA.cities.length})`;
      roleSel.appendChild(o);
    }
  }
  // If state.role is now hidden, fall back to first available
  if (!roleSel.querySelector(`option[value="${state.role}"]`)) {
    state.role = roleSel.options[0]?.value;
  }
  roleSel.value = state.role;

  // Build city dropdown
  const citySel = document.getElementById("city-pick");
  state.city = DATA.cities[0].city;
  for (const c of [...DATA.cities].sort((a, b) => a.city.localeCompare(b.city))) {
    const o = document.createElement("option");
    o.value = c.city;
    o.textContent = c.city + ", " + c.state;
    citySel.appendChild(o);
  }
  citySel.value = state.city;

  // Wire tabs
  document.querySelectorAll("nav.tabs button").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("nav.tabs button").forEach(b => b.classList.toggle("active", b === btn));
      document.querySelectorAll("section.tab").forEach(s => s.classList.toggle("active", s.id === "tab-" + btn.dataset.tab));
    });
  });
  document.getElementById("role-pick").addEventListener("change", e => { state.role = e.target.value; renderRole(); });
  document.getElementById("metric-pick").addEventListener("change", e => { state.metric = e.target.value; renderRole(); });
  document.getElementById("city-pick").addEventListener("change", e => { state.city = e.target.value; renderCity(); });
  document.getElementById("nyc-col").addEventListener("change", e => { state.nycCol = e.target.checked; renderNYC(); });
  document.getElementById("nyc-allin").addEventListener("change", e => { state.nycAllIn = e.target.checked; renderNYC(); });

  document.getElementById("compiled-date").textContent = DATA._metadata.compiled_date;

  renderRole();
  renderCity();
  renderNYC();
  renderMethodology();
})();

function renderNYC() {
  const summaryEl = document.getElementById("nyc-summary");
  const rankEl = document.getElementById("nyc-ranks");
  const rpps = DATA.rpp_2023;
  const nyc = DATA.cities.find(c => c.city === "New York");
  const colOn = state.nycCol;
  const allInOn = state.nycAllIn;

  // Helper: adjust a value for a city.
  const adj = (city, v) => {
    if (!colOn || v == null || !rpps[city]) return v;
    return v / (rpps[city] / 100);
  };

  // Build summary cards: NYC in plain English vs the 12-city set, per role per metric.
  const roleData = {};
  for (const [roleKey, roleLabel] of Object.entries(ROLE_LABELS)) {
    const cells = DATA.cities.map(c => {
      const r = c.roles[roleKey] || {};
      let topBase = r.top_base;
      if (allInOn && c.city === "New York") {
        const allIn = (DATA.nyc_all_in_estimates[roleKey] || {}).all_in_top_step;
        if (allIn != null) topBase = allIn;
      }
      return {
        city: c.city,
        entry_base: adj(c.city, r.entry_base),
        top_base: adj(c.city, topBase),
        years_to_top: r.years_to_top,
        excluded: (r.source_type === "private_contractor" || r.source_type === "needs_research"),
      };
    });
    roleData[roleKey] = cells;
  }

  // Header summary text
  const summaryLines = [];
  summaryLines.push(`<div style="background:var(--card);border:1px solid var(--line);border-radius:8px;padding:18px 22px;margin-bottom:16px;line-height:1.55">
    <div style="font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:0.04em">Setup</div>
    <div style="margin-top:6px">
      <strong>New York metro:</strong> 18.9M population (largest in dataset). NYC's BEA Regional Price Parity (2023) is <strong>${rpps["New York"]}</strong> &mdash; 12.6% above the U.S. average. Six of the 12 peer cities have a higher cost of living: SF (117.6), LA (114.7), Seattle (112.7), San Diego (110.7), Boston (110.4), DC (109.5).
    </div>
    <div style="margin-top:8px;color:var(--muted);font-size:13px">
      Toggle the <em>cost-of-living</em> checkbox above to compare in purchasing-power dollars (each city's wage divided by RPP/100).
      Toggle <em>NYC "all-in"</em> to swap NYC's contract base for the city's reported total compensation at top step (base + longevity + holiday pay + uniform allowance + night differential, excluding overtime).
    </div>
  </div>`);
  summaryEl.innerHTML = summaryLines.join("");

  // Per-role: NYC's rank for entry, top, years.
  const rankParts = [];
  for (const [roleKey, roleLabel] of Object.entries(ROLE_LABELS)) {
    const cells = roleData[roleKey];
    const nycCell = cells.find(c => c.city === "New York");
    if (!nycCell || nycCell.excluded || nycCell.top_base == null) {
      continue;  // skip roles without NYC data entirely (don't show empty blocks)
    }

    rankParts.push(buildRoleRankBlock(roleLabel, roleKey, cells, nycCell, allInOn));
  }
  rankEl.innerHTML = rankParts.join("");
}

function buildRoleRankBlock(roleLabel, roleKey, cells, nycCell, allInOn) {
  const validCells = cells.filter(c => !c.excluded);
  const metrics = [
    { key: "entry_base", label: "Entry-step base", fmt: fmt$, dir: "high-good" },
    { key: "top_base",   label: "Top-step base"  + (allInOn && DATA.nyc_all_in_estimates[roleKey] ? " (NYC: all-in)" : ""), fmt: fmt$, dir: "high-good" },
    { key: "years_to_top", label: "Years to top step", fmt: v => v + " yrs", dir: "low-good" },
  ];

  let html = `<div class="meta-block" style="margin-bottom:18px">
    <h2 style="font-size:17px;margin-bottom:4px">${roleLabel}</h2>`;

  // Per-metric rank summary
  html += `<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0">`;
  for (const m of metrics) {
    const sorted = validCells.filter(c => c[m.key] != null)
      .sort((a, b) => m.dir === "high-good" ? b[m.key] - a[m.key] : a[m.key] - b[m.key]);
    if (nycCell[m.key] == null) {
      html += `<div class="stat"><div class="label">${m.label}</div><div class="val muted">—</div><div class="sub">NYC not published</div></div>`;
      continue;
    }
    const rank = sorted.findIndex(c => c.city === "New York") + 1;
    const total = sorted.length;
    const nycVal = nycCell[m.key];
    const median = sortedMedian(sorted.map(c => c[m.key]));
    const top = sorted[0];
    const verb = m.dir === "high-good" ? "highest" : "fastest";
    const oppVerb = m.dir === "high-good" ? "lowest" : "slowest";
    let position;
    if (rank === 1) position = `<span style="color:var(--good)">${verb} of ${total}</span>`;
    else if (rank === total) position = `<span style="color:var(--bad)">${oppVerb} of ${total}</span>`;
    else if (rank <= total / 3) position = `<span style="color:var(--good)">top third (${rank} of ${total})</span>`;
    else if (rank > 2 * total / 3) position = `<span style="color:var(--bad)">bottom third (${rank} of ${total})</span>`;
    else position = `middle (${rank} of ${total})`;

    const vsMedian = m.key === "years_to_top"
      ? `${(nycVal - median).toFixed(1)} yrs vs. median ${median.toFixed(1)} yrs`
      : `${nycVal >= median ? "+" : ""}${fmt$(nycVal - median)} vs. median ${m.fmt(median)}`;
    const vsTop = m.key === "years_to_top"
      ? `${(nycVal - top[m.key]).toFixed(1)} yrs vs. ${top.city} (${m.fmt(top[m.key])})`
      : `${fmt$(nycVal - top[m.key])} vs. top: ${top.city} (${m.fmt(top[m.key])})`;
    html += `<div class="stat">
      <div class="label">${m.label}</div>
      <div class="val">${m.fmt(nycVal)}</div>
      <div class="sub" style="margin-top:6px">${position}</div>
      <div class="sub" style="margin-top:2px;font-size:11px">${vsMedian}</div>
      <div class="sub" style="font-size:11px">${vsTop}</div>
    </div>`;
  }
  html += `</div>`;

  // Bar chart of top base ranking the cities, NYC highlighted
  const sorted = validCells.filter(c => c.top_base != null).sort((a, b) => b.top_base - a.top_base);
  if (sorted.length) {
    const max = sorted[0].top_base;
    html += `<div style="font-size:12px;color:var(--muted);margin:14px 0 6px">Top-step base, all cities ranked (NYC highlighted)</div>`;
    html += sorted.map(c => {
      const isNYC = c.city === "New York";
      const w = (c.top_base / max) * 540;
      return `<div style="display:flex;align-items:center;height:22px;gap:6px">
        <div style="width:160px;font-size:13px;${isNYC ? "font-weight:600" : ""}">${c.city}</div>
        <div style="background:${isNYC ? "var(--hi)" : "var(--accent)"};opacity:${isNYC ? 1 : 0.55};height:11px;border-radius:2px;width:${w.toFixed(0)}px"></div>
        <div style="font-size:12px;color:${isNYC ? "var(--hi)" : "var(--muted)"};${isNYC ? "font-weight:600" : ""}">${fmt$(c.top_base)}</div>
      </div>`;
    }).join("");
  }
  html += `</div>`;
  return html;
}

function sortedMedian(arr) {
  const a = [...arr].filter(v => v != null).sort((x, y) => x - y);
  if (!a.length) return null;
  const mid = Math.floor(a.length / 2);
  return a.length % 2 ? a[mid] : (a[mid - 1] + a[mid]) / 2;
}

function renderRole() {
  const role = state.role;
  // Collect rows
  const rows = DATA.cities.map(c => {
    const r = c.roles[role] || {};
    return {
      city: c.city + ", " + c.state,
      cityRaw: c.city,
      msa_pop: c.msa_pop_million,
      entry_base: r.entry_base,
      top_base: r.top_base,
      years_to_top: r.years_to_top,
      source_url: r.source_url,
      cba_url: r.cba_url,
      source_type: r.source_type,
      effective_date: r.effective_date,
      union: r.union,
      agency: r.agency,
      notes: r.notes,
      max_with_longevity: r.max_with_longevity,
      max_years: r.max_years,
      comparison_basis: r.comparison_basis,
      pre_raise: r.pre_raise,
    };
  });

  // Compute averages excluding null and excluding "private_contractor" / "needs_research" rows
  const valid = rows.filter(r => r.source_type !== "private_contractor" && r.source_type !== "needs_research");
  const meanOf = key => {
    const vals = valid.map(r => r[key]).filter(v => v != null);
    return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : null;
  };
  const avgEntry = meanOf("entry_base");
  const avgTop = meanOf("top_base");
  const avgYrs = meanOf("years_to_top");

  // Stats
  const stats = document.getElementById("role-stats");
  stats.innerHTML = "";
  const card = (label, val, sub) => {
    const d = document.createElement("div");
    d.className = "stat";
    d.innerHTML = `<div class="label">${label}</div><div class="val">${val}</div><div class="sub">${sub || ""}</div>`;
    return d;
  };
  const nVals = valid.filter(r => r.top_base != null).length;
  stats.appendChild(card("Cities with data", nVals + " of " + DATA.cities.length, "where role exists & figure published"));
  stats.appendChild(card("Avg. entry base", fmt$(avgEntry), ""));
  stats.appendChild(card("Avg. top base", fmt$(avgTop), ""));
  stats.appendChild(card("Avg. years to top", avgYrs ? avgYrs.toFixed(1) + " yrs" : "—", ""));

  // Sort by metric desc; nulls last
  rows.sort((a, b) => {
    const va = a[state.metric], vb = b[state.metric];
    if (va == null && vb == null) return 0;
    if (va == null) return 1;
    if (vb == null) return -1;
    return vb - va;
  });

  // Table
  const tbody = document.querySelector("#tbl-role tbody");
  tbody.innerHTML = rows.map(r => {
    const tagInfo = SOURCE_TAGS[r.source_type] || { cls: "gap", text: r.source_type || "—" };
    const sourceCell = r.source_type === "private_contractor"
      ? `<span class="tag ${tagInfo.cls}">${tagInfo.text}</span>`
      : r.source_type === "needs_research"
        ? `<span class="tag ${tagInfo.cls}">${tagInfo.text}</span>` +
          (r.source_url ? `<br><a class="source-link" href="${r.source_url}" target="_blank" rel="noopener">lookup hint ↗</a>` : "")
        : `<a class="source-link" href="${r.source_url}" target="_blank" rel="noopener">${tagInfo.text} ↗</a>`;
    const note = r.notes ? `<details><summary>note</summary>${escapeHtml(r.notes)}</details>` : "";
    const cls = r.source_type === "private_contractor" ? "na" :
                (r.entry_base == null && r.top_base == null) ? "na" : "";
    const compBasisLabel = {
      post_progression_base: { text: "Post-step base", cls: "cba" },
      approximate: { text: "Approximate", cls: "dept" },
      partial: { text: "Partial", cls: "gap" },
      needs_research: { text: "Gap", cls: "gap" },
    }[r.comparison_basis] || null;
    const compBasisTag = compBasisLabel ? `<span class="tag ${compBasisLabel.cls}">${compBasisLabel.text}</span>` : "";
    const preRaiseTag = r.pre_raise ? `<span class="tag" style="background:#fef3c7;color:#92400e">Pre-raise</span>` : "";
    const employerTag = (r.employer_type && r.employer_type !== "city")
      ? `<span class="tag" style="background:#eef2ff;color:#3730a3">${r.employer_type.replace(/_/g, " ")}</span>`
      : "";
    const longCell = r.max_with_longevity != null
      ? `${fmt$(r.max_with_longevity)}${r.max_years ? ` <span class="muted" style="font-size:11px">@${r.max_years}yr</span>` : ""}`
      : (r.top_base != null ? `<span class="muted" style="font-size:12px">no longevity tier published</span>` : "—");
    return `<tr class="${cls}">
      <td>${r.city}${r.agency ? ` <span class="muted" style="font-size:11px">(${r.agency})</span>` : ""}</td>
      <td>${fmt$(r.entry_base)}</td>
      <td>${fmt$(r.top_base)}${r.years_to_top ? ` <span class="muted" style="font-size:11px">@${r.years_to_top}yr</span>` : ""}</td>
      <td>${fmtYrs(r.years_to_top)}</td>
      <td>${longCell}</td>
      <td class="l">${compBasisTag}${employerTag ? "<br>" + employerTag : ""}${preRaiseTag ? "<br>" + preRaiseTag : ""}</td>
      <td class="l">${sourceCell}${note}</td>
      <td class="l muted" style="font-size:12px">${r.effective_date || "—"}<br>${r.union || ""}</td>
    </tr>`;
  }).join("");

  // Bar chart
  renderBarChart(rows.filter(r => r[state.metric] != null), state.metric);
}

function renderBarChart(rows, metric) {
  const el = document.getElementById("bar-chart");
  if (!rows.length) { el.innerHTML = ""; return; }
  const max = Math.max(...rows.map(r => r[metric]));
  const fmt = metric === "years_to_top" ? (v => v + " yrs") : fmt$;
  el.innerHTML = `
    <div style="background:var(--card);border:1px solid var(--line);border-radius:8px;padding:16px">
      <div style="font-size:13px;color:var(--muted);margin-bottom:8px">
        ${metric === "entry_base" ? "Entry base" : metric === "top_base" ? "Top-step base" : "Years to top"} —
        cities with published figures, sorted high to low
      </div>
      ${rows.sort((a, b) => b[metric] - a[metric]).map(r => `
        <div class="bar">
          <div style="width:200px;font-size:13px">${r.city}</div>
          <div class="fill" style="width:${(r[metric] / max * 600).toFixed(0)}px"></div>
          <div class="label">${fmt(r[metric])}</div>
        </div>
      `).join("")}
    </div>
  `;
}

function renderCity() {
  const c = DATA.cities.find(x => x.city === state.city);
  if (!c) return;

  const stats = document.getElementById("city-stats");
  const card = (label, val, sub) => `<div class="stat"><div class="label">${label}</div><div class="val">${val}</div><div class="sub">${sub || ""}</div></div>`;
  stats.innerHTML = card("Metro", c.city + ", " + c.state, "")
    + card("MSA population", c.msa_pop_million.toFixed(1) + "M", "U.S. Census, MSA estimate");

  const tbody = document.querySelector("#tbl-city tbody");
  // Order roles by category then rank_order, using the registry
  let roleKeys;
  if (ROLE_REGISTRY) {
    const catOrder = ["Police", "Fire", "Sanitation", "Transit", "Education", "Other public sector"];
    const catIdx = k => catOrder.indexOf(ROLE_REGISTRY[k]?.category || "Other");
    roleKeys = Object.keys(ROLE_REGISTRY).sort((a, b) => {
      const ca = catIdx(a), cb = catIdx(b);
      if (ca !== cb) return ca - cb;
      return (ROLE_REGISTRY[a].rank_order || 0) - (ROLE_REGISTRY[b].rank_order || 0);
    });
  } else {
    roleKeys = Object.keys(ROLE_LABELS);
  }
  const rows = roleKeys.map(k => {
    const r = c.roles[k] || {};
    return { roleKey: k, roleLabel: ROLE_LABELS[k] || k, ...r };
  }).filter(r => r.top_base != null || r.entry_base != null || r.source_type === "private_contractor");
  tbody.innerHTML = rows.map(r => {
    const tagInfo = SOURCE_TAGS[r.source_type] || { cls: "gap", text: r.source_type || "—" };
    const sourceCell = r.source_type === "private_contractor"
      ? `<span class="tag ${tagInfo.cls}">${tagInfo.text}</span>`
      : r.source_type === "needs_research"
        ? `<span class="tag ${tagInfo.cls}">${tagInfo.text}</span>`
        : `<a class="source-link" href="${r.source_url}" target="_blank" rel="noopener">${tagInfo.text} ↗</a>`;
    const note = r.notes ? `<details><summary>note</summary>${escapeHtml(r.notes)}</details>` : "";
    const cls = (r.source_type === "private_contractor" || (r.entry_base == null && r.top_base == null)) ? "na" : "";
    return `<tr class="${cls}">
      <td>${r.roleLabel}${r.agency ? ` <span class="muted" style="font-size:11px">(${r.agency})</span>` : ""}</td>
      <td>${fmt$(r.entry_base)}</td>
      <td>${fmt$(r.top_base)}</td>
      <td>${fmtYrs(r.years_to_top)}</td>
      <td class="l">${sourceCell}${note}</td>
      <td class="l muted" style="font-size:12px">${r.effective_date || "—"}</td>
      <td class="l muted" style="font-size:12px">${r.union || "—"}</td>
    </tr>`;
  }).join("");
}

function renderMethodology() {
  const m = DATA._metadata;
  const el = document.getElementById("methodology");
  // Count cells with each source type
  const counts = {};
  for (const c of DATA.cities) {
    for (const role of Object.keys(ROLE_LABELS)) {
      const r = c.roles[role] || {};
      counts[r.source_type || "missing"] = (counts[r.source_type || "missing"] || 0) + 1;
    }
  }
  const countList = Object.entries(counts).sort((a, b) => b[1] - a[1])
    .map(([k, v]) => `<li><strong>${v}</strong> — ${k.replace(/_/g, " ")}</li>`).join("");

  // Source URLs grouped by city
  const sources = DATA.cities.map(c => {
    const links = Object.entries(c.roles).map(([role, r]) => {
      if (!r.source_url || r.source_type === "private_contractor") return null;
      return `<li>${ROLE_LABELS[role]}: <a href="${r.source_url}" target="_blank" rel="noopener">${r.source_url}</a>${r.cba_url && r.cba_url !== r.source_url ? ` &middot; <a href="${r.cba_url}" target="_blank" rel="noopener">CBA</a>` : ""}</li>`;
    }).filter(Boolean).join("");
    return `<h3 style="font-size:15px;margin-top:16px;margin-bottom:6px">${c.city}, ${c.state}</h3><ul>${links}</ul>`;
  }).join("");

  el.innerHTML = `
    <h2>Scope</h2>
    <p>${escapeHtml(m.scope)}</p>
    <h2>What is shown</h2>
    <p><strong>Salary basis:</strong> ${escapeHtml(m.salary_basis)}</p>
    <ul>
      ${Object.entries(m.roles_included).map(([k, v]) => `<li><strong>${ROLE_LABELS[k] || k}:</strong> ${escapeHtml(v)}</li>`).join("")}
    </ul>

    <h2>Important caveats</h2>
    <ul>${m.important_caveats.map(c => `<li>${escapeHtml(c)}</li>`).join("")}</ul>

    <h2>Employer types</h2>
    <p>Most roles in this dataset are city-employed, but several public services
       are delivered by other public bodies in particular metros. Cells are tagged with the
       relevant employer type when it isn't the city itself:</p>
    <ul>
      <li><strong>County</strong> — Public health nurses are typically employed by the
          county health department in major metros (LA County DPH, San Diego County
          HHSA, King County Public Health, Cook County Health, Harris County Public
          Health, Bexar County, Dallas County HHS, Maricopa County). Probation officers
          and tax assessors are also commonly county-employed.</li>
      <li><strong>Library system</strong> — NYC's three library systems (NYPL, BPL,
          Queens Library) are independent nonprofits with their own union contracts;
          librarians there are not city employees. Seattle Public Library and DC
          Public Library are similarly separate authorities.</li>
      <li><strong>Park district</strong> — Chicago Park District is independent of
          the City of Chicago.</li>
      <li><strong>School district</strong> — All teacher cells are school district
          employees, not city. NYC's DOE is technically a city agency but treated
          as a separate employer here.</li>
      <li><strong>Transit authority</strong> — Bus operators work for regional transit
          agencies (MTA, MBTA, SEPTA, WMATA, LA Metro, SFMTA, MTS, King County Metro,
          CTA, METRO Houston, DART, VIA, Valley Metro), not the city.</li>
      <li><strong>Private contractor</strong> — Sanitation in Boston, San Francisco
          and Seattle is performed by private firms (Capitol Waste Services, Recology,
          Waste Management). San Diego MTS and Phoenix Valley Metro contract bus
          operations to Transdev / First Transit.</li>
    </ul>

    <h2>Source-type tally (${DATA.cities.length} cities × ${Object.keys(ROLE_LABELS).length} roles = ${DATA.cities.length * Object.keys(ROLE_LABELS).length} cells)</h2>
    <ul>${countList}</ul>

    <h2>Why some cells are blank</h2>
    <p>Three reasons cells are blank:</p>
    <ul>
      <li><strong>Private contractor</strong> — for sanitation in Boston, San Francisco and Seattle, residential refuse collection is performed by private firms (Capitol Waste Services, Recology, Waste Management). For Phoenix transit and San Diego transit, bus operations are run by private contractors (Transdev, etc.). There are no city employees in those roles.</li>
      <li><strong>Scanned-image PDF</strong> — several CBAs (Phoenix PLEA pre-extraction, San Antonio police/fire) are scanned images, so dollar figures cannot be extracted programmatically. Where possible, equivalent figures were pulled from the city's HR salary report or department careers page; otherwise marked as a gap.</li>
      <li><strong>Not yet posted</strong> — Boston firefighter (new 4-yr CBA ratified Dec 2025; salary appendix not yet on boston.gov), Philadelphia firefighter (FY25+ successor under negotiation as of compilation date).</li>
    </ul>

    <h2>Sources by city</h2>
    ${sources}
  `;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"})[c]);
}
