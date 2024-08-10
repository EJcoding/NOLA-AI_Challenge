NOLA-AI Internship Challenge

Here's how I coded this challenge:

NOTE: I ran this easyocr solution on default CPU and not a GPU so there is possible performance difference if ran with a GPU (GPU could have better intended text extraction)

Firstly, I used VS Code so here's how to do it in this IDE

Open VS Code terminal

Create python venv using: 
python -m venv venv

Activate virtual environment:

windows: .\venv\Scripts\activate

macOS/Linux: source venv/bin/activate

Install libraries

pip install easyocr pillow python-dateutil fuzzywuzzy

To run script in terminal:

python main.py

*NOTE* when it asks img1 or img2, please type either 'img1' or 'img2' as the input

Here's some documentation of libraries I used:

https://github.com/JaidedAI/EasyOCR

https://pillow.readthedocs.io/en/stable/

https://dateutil.readthedocs.io/en/stable/

https://pypi.org/project/fuzzywuzzy/
