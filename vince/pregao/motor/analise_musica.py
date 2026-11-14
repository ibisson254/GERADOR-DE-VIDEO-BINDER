import librosa, numpy as np, json, sys
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units='time')
hop=512
rms = librosa.feature.rms(y=y, hop_length=hop)[0]
t = librosa.times_like(rms, sr=sr, hop_length=hop)
# low band energy
S = np.abs(librosa.stft(y, hop_length=hop))
freqs = librosa.fft_frequencies(sr=sr)
low = S[freqs<150].mean(0); high=S[freqs>4000].mean(0)
print("tempo", tempo, "beats", len(beats))
print("beats", np.round(beats,2).tolist())
# per half-second summary
for s in np.arange(0, 45.5, 0.5):
    m=(t>=s)&(t<s+0.5)
    if m.sum()==0: continue
    print(f"{s:5.1f} rms {rms[m].mean():.3f} low {low[m].mean():6.2f} high {high[m].mean():5.2f} onset {onset_env[m[:len(onset_env)]].max():5.1f}")
# strongest onsets
idx=np.argsort(onset_env)[::-1][:40]
tt=librosa.frames_to_time(idx, sr=sr, hop_length=hop)
print("top onsets", sorted(np.round(tt,2).tolist()))
