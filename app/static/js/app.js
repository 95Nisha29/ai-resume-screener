/**
 * TalentMatch AI - Recruiter Dashboard Frontend Logic
 */

let sampleData = null;
let currentJdId = "jd-fullstack";
let uploadedFiles = [];
let useDemoResumes = true;
let rankedResults = null;

// DOM Elements
const jdInput = document.getElementById("job-description-input");
const jdSkillsContainer = document.getElementById("jd-skills-container");
const jdSkillsCount = document.getElementById("jd-skills-count");
const jdExpBadge = document.getElementById("jd-exp-badge");
const presetButtons = document.getElementById("jd-preset-buttons");
const btnRefreshSkills = document.getElementById("btn-refresh-skills");

const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("resume-file-input");
const fileListContainer = document.getElementById("file-list-container");
const btnLoadDemoResumes = document.getElementById("btn-load-demo-resumes");

const toggleWeights = document.getElementById("toggle-weights");
const weightsBody = document.getElementById("weights-body");
const weightsChevron = document.getElementById("weights-chevron");
const sliderSim = document.getElementById("weight-sim");
const sliderSkill = document.getElementById("weight-skill");
const sliderExp = document.getElementById("weight-exp");
const valSim = document.getElementById("weight-sim-val");
const valSkill = document.getElementById("weight-skill-val");
const valExp = document.getElementById("weight-exp-val");

const btnRank = document.getElementById("btn-rank");
const resultsEmpty = document.getElementById("results-empty");
const resultsLoading = document.getElementById("results-loading");
const candidateList = document.getElementById("candidate-list");
const spotlightCard = document.getElementById("top-candidate-spotlight");
const searchInput = document.getElementById("candidate-search");
const btnExportCsv = document.getElementById("btn-export-csv");

// Modal Elements
const modal = document.getElementById("candidate-modal");
const modalClose = document.getElementById("modal-close");
const modalRankBadge = document.getElementById("modal-rank-badge");
const modalName = document.getElementById("modal-name");
const modalContact = document.getElementById("modal-contact");
const modalSimScore = document.getElementById("modal-sim-score");
const modalSkillScore = document.getElementById("modal-skill-score");
const modalOverallScore = document.getElementById("modal-overall-score");
const modalMatchedSkills = document.getElementById("modal-matched-skills");
const modalMissingSkills = document.getElementById("modal-missing-skills");
const modalMatchedCount = document.getElementById("modal-matched-count");
const modalMissingCount = document.getElementById("modal-missing-count");
const modalSnippet = document.getElementById("modal-snippet");

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", async () => {
  if (window.lucide) lucide.createIcons();
  await loadSampleData();
  setupEventListeners();
});

// Fetch pre-loaded samples from API
async function loadSampleData() {
  try {
    const res = await fetch("/api/samples");
    if (res.ok) {
      sampleData = await res.json();
      // Set initial JD to FullStack
      selectPreset("jd-fullstack");
    }
  } catch (err) {
    console.warn("Could not load sample data:", err);
  }
}

function selectPreset(presetId) {
  if (!sampleData || !sampleData.job_descriptions) return;
  const jd = sampleData.job_descriptions.find(j => j.id === presetId);
  if (jd) {
    currentJdId = presetId;
    jdInput.value = jd.description.trim();
    updatePresetButtonStyles(presetId);
    analyzeJobDescription(jd.description);
  }
}

function updatePresetButtonStyles(activeId) {
  const buttons = presetButtons.querySelectorAll("button");
  buttons.forEach(btn => {
    if (btn.dataset.preset === activeId) {
      btn.className = "preset-btn px-2.5 py-1 text-xs rounded-lg bg-indigo-500/20 text-indigo-300 border border-indigo-500/50 shadow-sm transition-all";
    } else {
      btn.className = "preset-btn px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-all";
    }
  });
}

// Analyze Job Description via API
async function analyzeJobDescription(text) {
  if (!text || text.trim().length < 10) {
    jdSkillsContainer.innerHTML = '<span class="text-xs text-slate-500 italic">Enter job description to see recognized skills.</span>';
    jdSkillsCount.textContent = "0";
    jdExpBadge.textContent = "Exp: Not stated";
    return;
  }

  const formData = new FormData();
  formData.append("job_description", text);

  try {
    const res = await fetch("/api/analyze-jd", {
      method: "POST",
      body: formData
    });
    if (res.ok) {
      const data = await res.json();
      renderJdSkills(data.skills);
      if (data.required_experience_years > 0) {
        jdExpBadge.textContent = `Exp: ${data.required_experience_years}+ yrs req.`;
        jdExpBadge.className = "text-xs px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 font-semibold border border-indigo-500/30";
      } else {
        jdExpBadge.textContent = "Exp: Open";
        jdExpBadge.className = "text-xs text-slate-400";
      }
    }
  } catch (err) {
    console.error("Error analyzing JD:", err);
  }
}

function renderJdSkills(skills) {
  jdSkillsCount.textContent = skills.length;
  if (!skills || skills.length === 0) {
    jdSkillsContainer.innerHTML = '<span class="text-xs text-slate-500 italic">No standard technical skills detected.</span>';
    return;
  }

  jdSkillsContainer.innerHTML = skills.map(skill => `
    <span class="inline-flex items-center px-2 py-0.5 rounded-md text-[11px] font-medium bg-slate-800 text-indigo-300 border border-slate-700">
      ${skill}
    </span>
  `).join("");
}

// Event Listeners Setup
function setupEventListeners() {
  // Preset buttons
  presetButtons.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (btn && btn.dataset.preset) {
      selectPreset(btn.dataset.preset);
    }
  });

  // JD Input debounce
  let debounceTimeout = null;
  jdInput.addEventListener("input", () => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
      analyzeJobDescription(jdInput.value);
    }, 500);
  });

  btnRefreshSkills.addEventListener("click", () => {
    analyzeJobDescription(jdInput.value);
  });

  // Weights toggle
  toggleWeights.addEventListener("click", () => {
    weightsBody.classList.toggle("hidden");
    weightsChevron.classList.toggle("rotate-180");
  });

  // Sliders sync
  sliderSim.addEventListener("input", () => valSim.textContent = `${sliderSim.value}%`);
  sliderSkill.addEventListener("input", () => valSkill.textContent = `${sliderSkill.value}%`);
  sliderExp.addEventListener("input", () => valExp.textContent = `${sliderExp.value}%`);

  // Drag and drop zone
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFilesSelected(Array.from(e.dataTransfer.files));
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFilesSelected(Array.from(e.target.files));
    }
  });

  // Demo Resumes button
  btnLoadDemoResumes.addEventListener("click", () => {
    useDemoResumes = true;
    uploadedFiles = [];
    fileListContainer.classList.remove("hidden");
    fileListContainer.innerHTML = `
      <div class="p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-400 flex items-center justify-between">
        <span class="flex items-center gap-1.5 font-medium">
          <i data-lucide="check-circle-2" class="w-4 h-4"></i>
          5 Demo Candidates Loaded (Alex, Elena, Marcus, Priya, Jordan)
        </span>
        <button type="button" id="clear-demo" class="text-[11px] text-slate-400 hover:text-white underline">Clear</button>
      </div>
    `;
    if (window.lucide) lucide.createIcons();
    document.getElementById("clear-demo").addEventListener("click", () => {
      useDemoResumes = false;
      fileListContainer.innerHTML = "";
      fileListContainer.classList.add("hidden");
    });
  });

  // Rank CTA button
  btnRank.addEventListener("click", executeScreening);

  // Search input filter
  searchInput.addEventListener("input", (e) => {
    filterCandidates(e.target.value);
  });

  // CSV Export
  btnExportCsv.addEventListener("click", exportResultsToCsv);

  // Modal close
  modalClose.addEventListener("click", () => modal.classList.add("hidden"));
  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.classList.add("hidden");
  });
}

function handleFilesSelected(files) {
  useDemoResumes = false;
  uploadedFiles = [...uploadedFiles, ...files];
  renderUploadedFilesList();
}

function renderUploadedFilesList() {
  if (uploadedFiles.length === 0) {
    fileListContainer.classList.add("hidden");
    fileListContainer.innerHTML = "";
    return;
  }

  fileListContainer.classList.remove("hidden");
  fileListContainer.innerHTML = uploadedFiles.map((f, i) => `
    <div class="flex items-center justify-between px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs">
      <span class="truncate max-w-[220px] text-slate-300 font-mono">${f.name}</span>
      <div class="flex items-center gap-2">
        <span class="text-[10px] text-slate-500">${(f.size / 1024).toFixed(1)} KB</span>
        <button type="button" onclick="removeFile(${i})" class="text-rose-400 hover:text-rose-300">
          <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
        </button>
      </div>
    </div>
  `).join("");

  if (window.lucide) lucide.createIcons();
}

window.removeFile = function(index) {
  uploadedFiles.splice(index, 1);
  renderUploadedFilesList();
};

// Execute Candidate Screening
async function executeScreening() {
  const jdText = jdInput.value.trim();
  if (!jdText) {
    alert("Please provide a Job Description (or choose a preset role).");
    return;
  }

  if (!useDemoResumes && uploadedFiles.length === 0) {
    alert("Please upload at least one resume file, or click 'Load 5 Demo Resumes'.");
    return;
  }

  // Set loading state
  resultsEmpty.classList.add("hidden");
  candidateList.classList.add("hidden");
  resultsLoading.classList.remove("hidden");
  btnRank.disabled = true;

  const wSim = parseFloat(sliderSim.value) / 100;
  const wSkill = parseFloat(sliderSkill.value) / 100;
  const wExp = parseFloat(sliderExp.value) / 100;

  try {
    let responseData = null;

    if (useDemoResumes && uploadedFiles.length === 0) {
      // Use rank-samples API
      const formData = new FormData();
      formData.append("sample_jd_id", currentJdId);
      formData.append("weight_similarity", wSim);
      formData.append("weight_skills", wSkill);
      formData.append("weight_experience", wExp);

      const res = await fetch("/api/rank-samples", {
        method: "POST",
        body: formData
      });
      responseData = await res.json();
    } else {
      // Use rank API with uploaded files
      const formData = new FormData();
      formData.append("job_description", jdText);
      uploadedFiles.forEach(file => {
        formData.append("resumes", file);
      });
      formData.append("weight_similarity", wSim);
      formData.append("weight_skills", wSkill);
      formData.append("weight_experience", wExp);

      const res = await fetch("/api/rank", {
        method: "POST",
        body: formData
      });
      responseData = await res.json();
    }

    resultsLoading.classList.add("hidden");
    btnRank.disabled = false;

    if (responseData && responseData.ranked_candidates) {
      rankedResults = responseData;
      renderScreeningResults(responseData);
      btnExportCsv.disabled = false;
    } else {
      alert("Screening failed. Please check your inputs.");
      resultsEmpty.classList.remove("hidden");
    }

  } catch (err) {
    console.error("Screening error:", err);
    resultsLoading.classList.add("hidden");
    btnRank.disabled = false;
    alert("An error occurred while screening candidates. See console for details.");
    resultsEmpty.classList.remove("hidden");
  }
}

// Render Results & Metrics
function renderScreeningResults(data) {
  const { summary_metrics, ranked_candidates } = data;

  // 1. Update Metrics Strip
  document.getElementById("stat-total").textContent = summary_metrics.total_candidates;
  document.getElementById("stat-top").textContent = `${summary_metrics.top_score}%`;
  document.getElementById("stat-avg").textContent = `${summary_metrics.avg_score}%`;
  document.getElementById("stat-strong").textContent = summary_metrics.strong_matches;

  // 2. Top Candidate Spotlight
  if (ranked_candidates.length > 0) {
    const topCand = ranked_candidates[0];
    spotlightCard.classList.remove("hidden");
    document.getElementById("spotlight-name").textContent = topCand.name;
    document.getElementById("spotlight-meta").textContent = 
      `${topCand.experience_years > 0 ? topCand.experience_years + ' yrs experience' : 'Experience detected'} • ${topCand.education}`;
    document.getElementById("spotlight-score").textContent = `${topCand.score}%`;

    const spotlightSkillsEl = document.getElementById("spotlight-skills");
    spotlightSkillsEl.innerHTML = topCand.matched_skills.slice(0, 6).map(s => `
      <span class="text-[11px] px-2 py-0.5 rounded-md bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
        <i data-lucide="check" class="w-3 h-3"></i> ${s}
      </span>
    `).join("");
  } else {
    spotlightCard.classList.add("hidden");
  }

  // 3. Render Candidate Cards
  renderCandidateCards(ranked_candidates);
  if (window.lucide) lucide.createIcons();
}

function renderCandidateCards(candidates) {
  candidateList.classList.remove("hidden");
  
  if (!candidates || candidates.length === 0) {
    candidateList.innerHTML = '<div class="py-8 text-center text-slate-500 text-xs">No matching candidates found for this filter.</div>';
    return;
  }

  candidateList.innerHTML = candidates.map(cand => {
    // Score Tier Colors
    let scoreBadgeBg = "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
    let progressBarBg = "bg-emerald-500";
    if (cand.score < 50) {
      scoreBadgeBg = "bg-rose-500/10 text-rose-400 border-rose-500/30";
      progressBarBg = "bg-rose-500";
    } else if (cand.score < 75) {
      scoreBadgeBg = "bg-amber-500/10 text-amber-400 border-amber-500/30";
      progressBarBg = "bg-amber-500";
    }

    const matchedPills = cand.matched_skills.slice(0, 5).map(s => `
      <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium bg-emerald-950/60 text-emerald-400 border border-emerald-800/60">
        <i data-lucide="check" class="w-2.5 h-2.5"></i> ${s}
      </span>
    `).join("");

    const missingPills = cand.missing_skills.slice(0, 4).map(s => `
      <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium bg-rose-950/40 text-rose-400 border border-rose-900/40">
        <i data-lucide="x" class="w-2.5 h-2.5"></i> ${s}
      </span>
    `).join("");

    return `
      <div class="glass-panel rounded-xl p-4 border border-slate-800 hover:border-slate-700 transition-all">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
          <div class="flex items-center gap-3">
            <span class="w-7 h-7 rounded-lg bg-slate-800 border border-slate-700 text-xs font-bold text-slate-300 flex items-center justify-center">
              #${cand.rank}
            </span>
            <div>
              <h4 class="text-sm font-semibold text-white hover:text-indigo-300 cursor-pointer" onclick="openCandidateModal('${cand.id}')">
                ${cand.name}
              </h4>
              <p class="text-[11px] text-slate-400">
                ${cand.experience_years > 0 ? cand.experience_years + ' yrs' : 'N/A'} • ${cand.education} • <span class="font-mono">${cand.filename}</span>
              </p>
            </div>
          </div>
          
          <div class="flex items-center gap-3 self-end sm:self-auto">
            <div class="text-right">
              <span class="text-xs font-semibold px-2.5 py-1 rounded-full border ${scoreBadgeBg}">
                ${cand.score}% Match
              </span>
            </div>
            <button 
              onclick="openCandidateModal('${cand.id}')"
              class="text-xs text-indigo-400 hover:text-indigo-300 px-2 py-1 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/20"
            >
              Details
            </button>
          </div>
        </div>

        <!-- Match Score Progress Bar -->
        <div class="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden mb-3">
          <div class="${progressBarBg} h-1.5 rounded-full transition-all duration-700" style="width: ${cand.score}%"></div>
        </div>

        <!-- Skills Summary Row -->
        <div class="space-y-1.5 pt-1 text-xs">
          ${cand.matched_skills.length > 0 ? `
            <div class="flex flex-wrap items-center gap-1.5">
              <span class="text-[10px] uppercase font-semibold text-emerald-500 mr-1">Matched:</span>
              ${matchedPills}
              ${cand.matched_skills.length > 5 ? `<span class="text-[10px] text-slate-400">+${cand.matched_skills.length - 5} more</span>` : ''}
            </div>
          ` : ''}

          ${cand.missing_skills.length > 0 ? `
            <div class="flex flex-wrap items-center gap-1.5">
              <span class="text-[10px] uppercase font-semibold text-rose-500 mr-1">Missing:</span>
              ${missingPills}
              ${cand.missing_skills.length > 4 ? `<span class="text-[10px] text-slate-400">+${cand.missing_skills.length - 4} more</span>` : ''}
            </div>
          ` : ''}
        </div>
      </div>
    `;
  }).join("");

  if (window.lucide) lucide.createIcons();
}

// Search / Filter
function filterCandidates(query) {
  if (!rankedResults || !rankedResults.ranked_candidates) return;
  const q = query.toLowerCase().trim();
  if (!q) {
    renderCandidateCards(rankedResults.ranked_candidates);
    return;
  }

  const filtered = rankedResults.ranked_candidates.filter(c => {
    const nameMatch = c.name.toLowerCase().includes(q);
    const skillMatch = c.matched_skills.some(s => s.toLowerCase().includes(q));
    const tierMatch = c.tier.toLowerCase().includes(q);
    return nameMatch || skillMatch || tierMatch;
  });

  renderCandidateCards(filtered);
}

// Open Detailed Candidate Modal
window.openCandidateModal = function(candidateId) {
  if (!rankedResults) return;
  const cand = rankedResults.ranked_candidates.find(c => c.id === candidateId);
  if (!cand) return;

  modalRankBadge.textContent = `#${cand.rank}`;
  modalName.textContent = cand.name;
  modalContact.textContent = `${cand.email || 'Email not detected'} | ${cand.phone || 'Phone not detected'}`;

  modalSimScore.textContent = `${cand.breakdown.similarity_score}%`;
  modalSkillScore.textContent = `${cand.breakdown.skill_score}%`;
  modalOverallScore.textContent = `${cand.score}%`;

  modalMatchedCount.textContent = cand.matched_skills.length;
  modalMissingCount.textContent = cand.missing_skills.length;

  modalMatchedSkills.innerHTML = cand.matched_skills.map(s => `
    <span class="px-2 py-1 rounded-md text-xs bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 flex items-center gap-1">
      <i data-lucide="check" class="w-3 h-3"></i> ${s}
    </span>
  `).join("") || '<span class="text-xs text-slate-500">None</span>';

  modalMissingSkills.innerHTML = cand.missing_skills.map(s => `
    <span class="px-2 py-1 rounded-md text-xs bg-rose-500/10 text-rose-300 border border-rose-500/20 flex items-center gap-1">
      <i data-lucide="x" class="w-3 h-3"></i> ${s}
    </span>
  `).join("") || '<span class="text-xs text-slate-500">None</span>';

  modalSnippet.textContent = cand.snippet;

  modal.classList.remove("hidden");
  modal.classList.add("flex");
  if (window.lucide) lucide.createIcons();
};

// Export to CSV
function exportResultsToCsv() {
  if (!rankedResults || !rankedResults.ranked_candidates) return;

  const headers = [
    "Rank",
    "Candidate Name",
    "Overall Match Score (%)",
    "Tier",
    "Similarity Score (%)",
    "Skill Score (%)",
    "Experience Score (%)",
    "Detected Experience (Yrs)",
    "Education",
    "Email",
    "Phone",
    "Matched Skills",
    "Missing Skills"
  ];

  const rows = rankedResults.ranked_candidates.map(c => [
    c.rank,
    `"${c.name}"`,
    c.score,
    `"${c.tier}"`,
    c.breakdown.similarity_score,
    c.breakdown.skill_score,
    c.breakdown.experience_score,
    c.experience_years,
    `"${c.education}"`,
    `"${c.email || ''}"`,
    `"${c.phone || ''}"`,
    `"${c.matched_skills.join(', ')}"`,
    `"${c.missing_skills.join(', ')}"`
  ]);

  const csvContent = "data:text/csv;charset=utf-8," 
    + [headers.join(","), ...rows.map(e => e.join(","))].join("\n");

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `Candidate_Rankings_${new Date().toISOString().slice(0,10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
