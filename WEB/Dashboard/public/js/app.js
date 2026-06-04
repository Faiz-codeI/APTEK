// ===== Splash Screen Logic =====
function closeSplash() {
    const splash = document.getElementById('splashScreen');
    splash.classList.add('hidden');
    
    // Add a slight delay before triggering the first preview so it feels alive
    setTimeout(() => {
        triggerPreview();
    }, 600);
}

// ===== Mood Logic =====
let currentMood = null;

function selectMood(element, mood) {
    // Remove selected class from all buttons
    document.querySelectorAll('.mood-btn').forEach(btn => btn.classList.remove('selected'));
    
    // Add selected class to clicked button
    element.classList.add('selected');
    currentMood = mood;
    
    // Slight tweak to companion based on mood before checking sliders
    const emoji = document.getElementById('companionEmoji');
    if(mood === 'Senang') {
        emoji.textContent = '🌟';
    } else if(mood === 'Lelah') {
        emoji.textContent = '🥱';
    } else if(mood === 'Cemas') {
        emoji.textContent = '🥀';
    } else {
        emoji.textContent = '🌿';
    }
}

// ===== Navigation =====
function navigateTo(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.sidebar-menu a').forEach(a => a.classList.remove('active'));

    document.getElementById(pageId).classList.add('active');
    document.querySelector(`[data-page="${pageId}"]`).classList.add('active');
}

// ===== Slider value updater =====
function updateSlider(sliderId, badgeId, suffix) {
    const val = document.getElementById(sliderId).value;
    const formatted = (suffix === ' Jam') ? parseFloat(val).toFixed(1) : val;
    document.getElementById(badgeId).textContent = formatted + suffix;
}

// ===== Companion Logic (Dynamic feedback without API for instant preview) =====
function triggerPreview() {
    // If user selected a mood, don't overwrite it immediately unless sliders change drastically
    const screentime = parseFloat(document.getElementById('sl_screen').value);
    const unlocks = parseInt(document.getElementById('sl_unlock').value);
    const sleep = parseFloat(document.getElementById('sl_sleep').value);
    
    const emoji = document.getElementById('companionEmoji');
    const compCard = document.querySelector('.companion-card');
    
    // Simple heuristic for immediate visual feedback before clicking the button
    let score = 0;
    if (screentime > 8) score += 1;
    if (unlocks > 80) score += 1;
    if (sleep < 6) score += 2;
    
    // Reset classes
    emoji.className = 'companion-emoji';
    compCard.className = 'card companion-card';
    
    if (score >= 3) {
        if(currentMood !== 'Cemas') emoji.textContent = '🥀'; 
        emoji.classList.add('state-danger');
        compCard.classList.add('danger');
    } else if (score >= 1) {
        if(currentMood !== 'Lelah' && currentMood !== 'Cemas') emoji.textContent = '🍂';
        emoji.classList.add('state-warning');
        compCard.classList.add('warning');
    } else {
        if(!currentMood || currentMood === 'Biasa') emoji.textContent = '🌿';
        emoji.classList.add('state-success');
        compCard.classList.add('success');
    }
}

// ===== Prediction =====
async function runPrediction() {
    const screentime = parseFloat(document.getElementById('sl_screen').value);
    const unlocks = parseInt(document.getElementById('sl_unlock').value);
    const sleep = parseFloat(document.getElementById('sl_sleep').value);
    const conversation = parseFloat(document.getElementById('sl_conv').value);
    const model = document.getElementById('sel_model').value; 

    const btn = document.querySelector('.btn-primary');
    btn.textContent = '⏳ Menghubungi AI...';
    btn.disabled = true;

    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ screentime, unlocks, sleep, conversation, model })
        });

        const data = await res.json();
        showCompanionResult(data);
    } catch (err) {
        alert('Error koneksi ke server: ' + err.message);
    }

    btn.textContent = '✨ Evaluasi Kondisiku';
    btn.disabled = false;
}

function showCompanionResult(data) {
    const emoji = document.getElementById('companionEmoji');
    const statusText = document.getElementById('companionStatus');
    const riskBarContainer = document.getElementById('riskBarContainer');
    const riskBar = document.getElementById('riskBar');
    const recBox = document.getElementById('companionRec');
    const compCard = document.querySelector('.companion-card');
    
    // Reset styles
    emoji.className = 'companion-emoji';
    compCard.className = 'card companion-card';
    
    riskBarContainer.style.display = 'block';
    riskBar.style.width = `${data.probability}%`;
    
    recBox.style.display = 'block';
    recBox.textContent = data.recommendation;

    if (data.level === 'danger') {
        emoji.textContent = '🥀';
        emoji.classList.add('state-danger');
        compCard.classList.add('danger');
        riskBar.style.backgroundColor = 'var(--danger)';
        statusText.innerHTML = `<h3>Waduh, aku layu... 😢</h3><p>Baterai mentalku terkuras (${data.probability}% Risiko Stres).</p>`;
    } else if (data.level === 'warning') {
        emoji.textContent = '🍂';
        emoji.classList.add('state-warning');
        compCard.classList.add('warning');
        riskBar.style.backgroundColor = 'var(--warning)';
        statusText.innerHTML = `<h3>Aku butuh air (istirahat)... 🥱</h3><p>Kondisiku agak menurun nih (${data.probability}% Risiko Stres).</p>`;
    } else {
        emoji.textContent = '🌿';
        emoji.classList.add('state-success');
        compCard.classList.add('success');
        riskBar.style.backgroundColor = 'var(--success)';
        statusText.innerHTML = `<h3>Aku segar banget! 🌟</h3><p>Terima kasih sudah menjaga keseimbangan harimu! (${data.probability}% Risiko Stres).</p>`;
    }
}

// ===== Init =====
document.addEventListener('DOMContentLoaded', () => {
    navigateTo('page-simulator');
    // We don't triggerPreview() immediately so the splash screen doesn't cause background glitches
});

// ===== Model Selection Handler =====
function selectModel(model) {
    document.querySelectorAll('.segmented-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-value') === model) {
            btn.classList.add('active');
        }
    });
    document.getElementById('sel_model').value = model;
    
    // Auto prediction trigger when changing model to instantly update the UI feedback
    runPrediction();
}

// ===== Mock Report Downloads =====
function downloadReport(type) {
    if (type === 'csv') {
        const csvContent = "data:text/csv;charset=utf-8," 
            + "UID,Screentime (Jam/Hari),Unlock (Kali/Hari),Tidur (Jam/Malam),Durasi Sosial (Menit/Hari),Label Risiko\n"
            + "u01,6.8,85,5.2,45,1\n"
            + "u02,3.2,30,7.5,120,0\n"
            + "u03,7.5,92,4.8,15,1\n"
            + "u04,4.1,42,6.8,90,0\n";
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "CareSense_Sensor_Data_StudentLife.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } else {
        alert('📄 Fitur unduh laporan PDF sedang disiapkan. Laporan ringkas berisi analisis deskriptif data StudentLife akan dikirim ke email konselor.');
    }
}

// ===== Counseling Appointment Scheduler =====
function handleCounselingSubmit(event) {
    event.preventDefault();
    const date = document.getElementById('counselingDate').value;
    const time = document.getElementById('counselingTime').value;
    const notes = document.getElementById('counselingNotes').value;
    
    const successMsg = document.getElementById('counselingSuccessMsg');
    successMsg.style.display = 'block';
    successMsg.style.animation = 'fadeInPage 0.5s ease forwards';
    
    // Reset form
    document.getElementById('counselingForm').reset();
    
    // Hide success message after 5 seconds
    setTimeout(() => {
        successMsg.style.display = 'none';
    }, 5000);
}
