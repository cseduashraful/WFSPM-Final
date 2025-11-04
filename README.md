# WFSPM-Final  
**Implementation of “Weighted Frequent Sequential Pattern Mining”**

**Reference Paper:**  
Md Ashraful Islam, Mahfuzur Rahman Rafi, Al-amin Azad & Jesan Ahammed Ovi.  
*Weighted frequent sequential pattern mining.*  
Applied Intelligence (Springer), Vol. 52, pp. 254-281 (2022).  
[📄 Read the Paper on Springer](https://doi.org/10.1007/s10489-021-02290-w)

---

## 🎯 Overview  
This repository contains the official implementation of the **Weighted Frequent Sequential Pattern Mining (WFSPM)** algorithm described in the above paper.  
WFSPM mines **sequential patterns** from a sequence database while assigning **weights** to items (or events) to represent their relative importance.  
By introducing **weight-aware pruning techniques**, the method effectively reduces the search space and improves execution time without losing completeness.

---

## 📁 Repository Structure
```
├── algo/                  → core algorithm implementation  
├── data/                  → example datasets / sequence data  
├── output/graphs/         → runtime and pattern-count plots  
├── utility/               → helper utilities for preprocessing  
├── main.py                → main entry script  
├── evaluation.py          → evaluation metrics and comparison code  
├── graph.py               → visualization and graph generation  
├── addWeightSeq.py        → assign weights to sequence items  
└── spmf.jar               → baseline sequential pattern miner
```

---

## ⚙️ Requirements
- Python 3.x  
- Libraries: `numpy`, `pandas`, `matplotlib` (and any others required by your scripts)  
- Java 8+ (for running `spmf.jar` baseline experiments)

---

## 🚀 Usage

### 1️⃣ Prepare weighted sequences
```bash
python addWeightSeq.py --input data/sample.txt --output data/weighted_sample.txt --weights weights.txt
```

### 2️⃣ Run WFSPM
```bash
python main.py --input data/weighted_sample.txt --min_sup 0.01 --min_weight 5
```

### 3️⃣ Evaluate and visualize
```bash
python evaluation.py
```
Results and graphs are saved under `output/graphs/`.

---

## 📊 Results Summary  
The experiments in the paper demonstrate that WFSPM:
- Produces significantly fewer candidate patterns than comparable algorithms  
- Executes faster on both synthetic and real-world datasets  
- Preserves pattern completeness while achieving substantial pruning efficiency  

Refer to the paper for detailed quantitative results and comparative analysis.

---

## 📘 Citation  
If you use this repository or algorithm in your research, please cite the original paper:

> Islam, M.A., Rafi, M.R., Azad, A., & Ovi, J.A. (2022). Weighted Frequent Sequential Pattern Mining.  
> *Applied Intelligence*, 52, 254–281. https://doi.org/10.1007/s10489-021-02290-w

---

## 🤝 Contributing  
Pull requests and improvements are welcome!  
Please describe any proposed changes clearly and include sample results when possible.

---

## 📄 License  
Specify your license here (for example, **MIT License**) or note if none.

---

## 📬 Contact  
**Md Ashraful Islam**  
University of Dhaka, Bangladesh  
GitHub: [cseduashraful](https://github.com/cseduashraful)
