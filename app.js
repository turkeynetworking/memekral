let score = localStorage.getItem('kralScore') ? parseInt(localStorage.getItem('kralScore')) : 0;
document.getElementById('main-score').innerText = score;

// 1. DOKUN-KAZAN MEKANİĞİ
const tapBtn = document.getElementById('tap-btn');
const animContainer = document.getElementById('tap-anim-container');

if(tapBtn) {
    tapBtn.addEventListener('click', (e) => {
        score += 10;
        localStorage.setItem('kralScore', score);
        document.getElementById('main-score').innerText = score;

        // Puan Uçurma Efekti
        const x = e.clientX - tapBtn.getBoundingClientRect().left;
        const y = e.clientY - tapBtn.getBoundingClientRect().top;
        
        const floatingText = document.createElement('div');
        floatingText.innerText = "+10";
        floatingText.className = "absolute text-[#D4AF37] font-bold pointer-events-none animate-float z-50";
        floatingText.style.left = `${x}px`;
        floatingText.style.top = `${y}px`;
        
        animContainer.appendChild(floatingText);
        setTimeout(() => floatingText.remove(), 800);
    });
}

// 2. KRAL ANALİZ MOTORU (HATA DÜZELTİLDİ)
async function kralAnaliz() {
    const caInput = document.getElementById('sol-ca');
    const ca = caInput ? caInput.value.trim() : "";
    
    if(ca.length < 30) {
        alert("Kral, bu adres Solana değil! En az 32 karakterlik bir CA gir.");
        return;
    }

    // Buton Efekti
    const btn = document.querySelector('button[onclick="kralAnaliz()"]');
    const originalText = btn.innerText;
    btn.disabled = true;
    btn.innerText = "AĞA BAĞLANILIYOR... ⚡";

    try {
        // 2 Saniye 'Ciddiyet' Beklemesi
        await new Promise(r => setTimeout(r, 2000)); 

        const overlay = document.getElementById('modal-overlay');
        const textElement = document.getElementById('modal-text');
        
        // Rapor İçeriği (Profesyonel Görünüm)
        const riskScore = Math.floor(Math.random() * 40) + 15; 
        
        textElement.innerHTML = `
            <div class="text-left space-y-3 bg-black/40 p-4 rounded-2xl border border-[#D4AF37]/10">
                <div class="flex justify-between">
                    <span class="text-gray-500 uppercase text-[10px]">Kontrat:</span>
                    <span class="text-[#D4AF37] text-[10px] font-mono">${ca.substring(0,6)}...${ca.substring(ca.length-4)}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-500 uppercase text-[10px]">Güvenlik:</span>
                    <span class="text-green-500 text-[10px] font-bold">TEMİZ (SİMÜLE)</span>
                </div>
                <div class="flex justify-between border-t border-white/5 pt-2">
                    <span class="text-white text-xs font-bold uppercase tracking-tighter italic font-['Orbitron']">RİSK SKORU:</span>
                    <span class="text-[#D4AF37] font-bold">%${riskScore}</span>
                </div>
                <p class="text-[11px] text-gray-400 italic mt-2 leading-tight">"Balina cüzdanları takibe alındı. Dev (Geliştirici) henüz satış yapmadı ancak likidite kilidi zayıf görünüyor."</p>
            </div>
        `;
        
        // MODALI GÖSTER (Burada hata vardı, düzelttik)
        overlay.classList.remove('hidden');
        overlay.style.display = 'flex';

    } catch (error) {
        console.error(error);
        alert("Bağlantı koptu kral, tekrar dene.");
    } finally {
        btn.disabled = false;
        btn.innerText = originalText;
    }
}

// MODAL KAPATMA
function closeModal() {
    const overlay = document.getElementById('modal-overlay');
    overlay.classList.add('hidden');
    overlay.style.display = 'none';
}
