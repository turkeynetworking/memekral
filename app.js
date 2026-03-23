let score = 0;

// Dokun-Kazan Fonksiyonu
document.getElementById('tap-btn').addEventListener('click', () => {
    score += 10;
    alert("Tebrikler Kral! 10 Puan Kazandın. Toplam: " + score);
    // Buraya ileride puanları veritabanına kaydetme kodu gelecek
});

// Analiz Fonksiyonu (Simülasyon)
function analizEt() {
    const ca = document.querySelector('input').value;
    if(ca.length < 30) {
        alert("Geçersiz Solana Adresi! Kral hata sevmez.");
        return;
    }
    
    alert("Kral Analiz Başlıyor... Kontrat taranıyor: " + ca);
    
    // Buraya gerçek RugCheck API'sini bağlayacağız kanka
    setTimeout(() => {
        alert("ANALİZ SONUCU: Likidite Kilitleme %90, Risk Düşük! Bu proje 'Meme Kral' onayı alabilir.");
    }, 2000);
}