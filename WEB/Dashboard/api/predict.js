module.exports = (req, res) => {
    if (req.method === 'POST') {
        const { screentime, unlocks, sleep, conversation, model } = req.body;

        // Simulasi z-score normalization (berdasarkan statistik dataset)
        const z_screen = (screentime - 4.5) / 2.0;
        const z_unlocks = (unlocks - 35) / 15.0;
        const z_sleep = (sleep - 6.5) / 1.5;
        const z_conv = (conversation - 50) / 25.0;

        let score;
        if (model === 'rf') {
            // Random Forest: bobot dari feature importance
            score = (z_screen * 0.355) + (z_unlocks * 0.356) - (z_sleep * 0.289) - (z_conv * 0.001);
        } else {
            // SVM: bobot lebih merata
            score = (z_screen * 0.30) + (z_unlocks * 0.25) - (z_sleep * 0.25) - (z_conv * 0.20);
        }

        // Sigmoid -> probabilitas
        const probability = 1 / (1 + Math.exp(-score));
        const probPercent = Math.round(probability * 100);

        let status, level, recommendation;
        if (probPercent >= 60) {
            status = 'Risiko Tinggi';
            level = 'danger';
            recommendation = 'Pola tidur Anda sangat kurang dan screen-time berlebih. Disarankan untuk segera mengurangi penggunaan gadget sebelum tidur, tingkatkan durasi tidur malam minimal 7 jam, dan pertimbangkan untuk menghubungi layanan konseling kampus.';
        } else if (probPercent >= 40) {
            status = 'Risiko Sedang';
            level = 'warning';
            recommendation = 'Beberapa indikator menunjukkan ketidakseimbangan pola hidup harian. Cobalah untuk meningkatkan kualitas tidur, kurangi frekuensi membuka layar HP secara impulsif, dan luangkan waktu untuk bersosialisasi.';
        } else {
            status = 'Normal / Sehat';
            level = 'success';
            recommendation = 'Pola perilaku harian Anda tergolong seimbang dan sehat. Pertahankan durasi tidur yang cukup dan interaksi sosial aktif Anda.';
        }

        return res.status(200).json({
            probability: probPercent,
            status,
            level,
            recommendation,
            model_used: model === 'rf' ? 'Random Forest (Akurasi: 80%)' : 'SVM (Akurasi: 53%)'
        });
    } else {
        return res.status(405).json({ error: 'Method not allowed' });
    }
};
