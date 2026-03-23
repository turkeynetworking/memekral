// Skor Yönetimi
let score = localStorage.getItem('kralScore') ? parseInt(localStorage.getItem('kralScore')) : 0;
document.getElementById('main-score').innerText = score;

// 1. DOKUN-KAZAN
const tapBtn = document.getElementById('tap-btn');
const animContainer = document.getElementById('tap-anim-container');

tapBtn.addEventListener('click', (e) => {
    score += 10;
    localStorage.setItem('kralScore', score);
    document.getElementById('main-score').innerText = score;

    // Puan Uçurma Efekti
    const rect = tapBtn.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const floatingText = document.createElement('div');
    floatingText.innerText = "+10";
    floatingText.className = "absolute text-[#D4AF37] font-bold pointer-events-none z-50 animate-float";
    floatingText.style.left = `${x}px`;
    floatingText.style.top = `${y}px`;
    
    animContainer.appendChild(floatingText);
    setTimeout(() => floatingText.remove(), 800);
});

// 2. ANALİZ MOTORU
async function kralAnaliz() {
    const ca = document.getElementById('sol-ca').value.trim();
    const btn = document.getElementById('analiz-btn');
    
    if(ca.length < 30) {
        alert("Kral, geçerli bir Solana CA gir!");
        return;
    }

    btn.disabled = true;
    btn.innerText = "TARANIYOR... 🔍";

    // 2 saniye bekleme
    await new Promise(r => setTimeout(r, 2000));

    const overlay = document.getElementById('modal-overlay');
    const textElement = document.getElementById('modal-text');
    
    textElement.innerHTML = `
        <div class="bg-black/50 p-4 rounded-xl border border-white/5 text-left">
            <p class="mb-2">💎 <span class="text-[#D4AF37]">Likidite:</span> %88 Kilitli</p>
            <p class="mb-2">🐋 <span class="text-[#D4AF37]">Balina:</span> Hareket Var</p>
            <p>⚠️ <span class="text-[#D4AF37]">Risk:</span> Orta Seviye</p>
            <p class="mt-4 italic text-[10px] text-gray-500 text-center text-white">"Dev (Geliştirici) cüzdanı takipte! VIP raporu ile satış yapıp yapmayacağını gör."</p>
        </div>
    `;

    overlay.classList.remove('hidden');
}

function closeModal() {
    document.getElementById('modal-overlay').classList.add('hidden');
}
