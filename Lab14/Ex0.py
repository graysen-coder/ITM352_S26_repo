#Write Python code that checks if the SciPy, statsmodels, matplotlib packages are installed
try:    
    import scipy
    print("SciPy is installed.")
except ImportError:
    print("SciPy is not installed.")

try:
    import statsmodels
    print("statsmodels is installed.")
except ImportError:
    print("statsmodels is not installed.")

try:
    import matplotlib
    print("matplotlib is installed.")
except ImportError:
    print("matplotlib is not installed.")