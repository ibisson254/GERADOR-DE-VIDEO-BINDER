@echo off
rem Vince Vault · instala ComfyUI + TRELLIS.2 (suporte nativo) num PC Windows com placa NVIDIA.
rem Usado a 09/11/2026 no PC do fundador (RTX 3060 12 GB, Python 3.12, driver 560.94).
rem Requisitos: git e Python 3.12 (py launcher). Muda ROOT se quiser outro disco.
set ROOT=E:\ComfyUI
set CACHE=E:\ComfyUI_cache
set PIP_CACHE_DIR=%CACHE%\pip
set HF_HOME=%CACHE%\hf
set TMP=%CACHE%\tmp
set TEMP=%CACHE%\tmp
mkdir "%CACHE%\tmp" 2>nul

echo [1/6] clonar ComfyUI
if not exist "%ROOT%\main.py" git clone --depth 1 https://github.com/Comfy-Org/ComfyUI.git "%ROOT%" || goto :erro
cd /d "%ROOT%"
echo [2/6] ambiente Python 3.12
if not exist "%ROOT%\venv\Scripts\python.exe" py -3.12 -m venv venv || goto :erro
set PY=%ROOT%\venv\Scripts\python.exe
"%PY%" -m pip install --upgrade pip
echo [3/6] PyTorch CUDA 12.6 (driver NVIDIA 560+)
"%PY%" -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126 || goto :erro
echo [4/6] dependencias do ComfyUI
"%PY%" -m pip install -r requirements.txt || goto :erro
echo [5/6] ComfyUI-Manager
if not exist "%ROOT%\custom_nodes\ComfyUI-Manager" git clone --depth 1 https://github.com/Comfy-Org/ComfyUI-Manager.git "%ROOT%\custom_nodes\ComfyUI-Manager"
"%PY%" -m pip install -r "%ROOT%\custom_nodes\ComfyUI-Manager\requirements.txt"

echo [6/6] modelos do TRELLIS.2 (~9 GB; o Hugging Face corta ligacoes, o ciclo retoma sozinho)
call :baixar vae trellis_2_texture_vae_bf16.safetensors https://huggingface.co/Comfy-Org/Pixal3D/resolve/main/vae/trellis_2_texture_vae_bf16.safetensors
call :baixar vae trellis_2_shape_vae_bf16.safetensors https://huggingface.co/Comfy-Org/Pixal3D/resolve/main/vae/trellis_2_shape_vae_bf16.safetensors
call :baixar clip_vision dino_v3_L_naf_fp32.safetensors https://huggingface.co/Comfy-Org/Pixal3D/resolve/main/clip_vision/dino_v3_L_naf_fp32.safetensors
call :baixar geometry_estimation moge_2_vitl_normal_fp16.safetensors https://huggingface.co/Comfy-Org/MoGe/resolve/main/geometry_estimation/moge_2_vitl_normal_fp16.safetensors
call :baixar background_removal birefnet.safetensors https://huggingface.co/Comfy-Org/BiRefNet/resolve/main/background_removal/birefnet.safetensors
call :baixar diffusion_models trellis_2_int8_convrot.safetensors https://huggingface.co/Comfy-Org/TRELLIS.2/resolve/main/diffusion_models/trellis_2_int8_convrot.safetensors
rem O workflow oficial tambem referencia o Pixal3D (5,2 GB). Nao e preciso: ligacao fisica ao TRELLIS.2 so para validar.
if not exist "%ROOT%\models\diffusion_models\pixal3d_int8_convrot.safetensors" mklink /H "%ROOT%\models\diffusion_models\pixal3d_int8_convrot.safetensors" "%ROOT%\models\diffusion_models\trellis_2_int8_convrot.safetensors"

"%PY%" -c "import torch;print('TORCH',torch.__version__,'CUDA',torch.cuda.is_available())"
echo INSTALACAO_OK
goto :eof

:baixar
mkdir "%ROOT%\models\%1" 2>nul
:loop_%2
curl -L -C - --retry 5 -sS --speed-limit 20000 --speed-time 60 -o "%ROOT%\models\%1\%2" "%3"
if errorlevel 1 (timeout /t 5 /nobreak >nul & goto :loop_%2)
echo OK %2
goto :eof

:erro
echo INSTALACAO_FALHOU
