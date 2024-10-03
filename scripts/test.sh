if [ -d ".conda" ]; then
  rm -r .conda
fi

conda create -p .conda 
conda activate .conda

pip install git+https://github.com/djoroya/djlmp.git

cd .. 

python -c "from djlmp.djlmp import djlmp"
