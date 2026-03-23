
let score = localStorage.getItem('kralScore') ? parseInt(localStorage.getItem('kralScore')) : 0;
document.getElementById('main-score').innerText = score;

// Dokun-Kazan Mekaniği + Animasyon
const tapBtn = document.getElementById('tap-btn');
const animContainer = document.getElementById('tap-anim-container');

tapBtn.addEventListener('click', (e) => {
    score += 10;
    localStorage.setItem('kralScore', score);
    document.getElementById('main-score').innerText = score;

    // Altın Puan Uçurma Efekti
    const x = e.clientX - tapBtn.getBoundingClientRect().left;
    const y = e.clientY - tapBtn.getBoundingClientRect().top;
    
    const floatingText = document.createElement('div');
    floatingText.innerText = "+10";
    floatingText.className = "absolute text-[#D4AF37] font-bold pointer-events-none animate-float";
    floatingText.style.left = `${x}px`;
    floatingText.style.top = `${y}px`;
    
    animContainer.appendChild(floatingText);
    setTimeout(() => floatingText.remove(), 800);
});

// Kral Analiz Simülasyonu
async function kralAnaliz() {
    const ca = document.getElementById('sol-ca').value;
    
    if(ca.length < 30) {
        alert("Kanka bu adres Solana değil! Kralı kandıramazsın.");
        return;
    }

    // Modal Penceresini Aç
    const overlay = document.getElementById('modal-overlay');
    const text = document.getElementById('modal-text');
    
    text.innerText = "Temel tarama bitti: Balina cüzdanlarında hareket var! Rug-Pull riski %35 görünüyor. Kesin sonuç için VIP raporu almalısın.";
    overlay.classList.remove('hidden');
    overlay.classList.add('flex');
}

function closeModal() {
    document.getElementById('modal-overlay').classList.add('hidden');
    document.getElementById('modal-overlay').classList.remove('flex');
}
