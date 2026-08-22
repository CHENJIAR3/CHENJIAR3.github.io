---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>
# ⏩ About me
My name is Jiarong Chen. I am currently a Ph.D. student at Shanghai Jiao Tong University, where I am pursuing my doctoral degree under the supervision of Prof. Guoxing Wang.  I received both my Bachelor's and Master's degrees in Biomedical Engineering from Sun Yat-sen University. I was twice awarded the National Scholarship and was also recognized as an Outstanding Graduate of Sun Yat-sen University. My research focuses on wearable sensing and AI for healthcare, with particular interests in cardiovascular monitoring, photoplethysmography (PPG), electrocardiography (ECG), cuffless blood pressure estimation, and multimodal physiological signal analysis. 
I have published my research findings in several international journals, including npj Digitial Medicine, Advanced Science, IEEE Journal of Biomedical and Health Informatics, Expert Systems With Applications, Biomedical Signal Processing and Control, Applied Soft Computing, IEEE Transactions on Instrumentation and Measurement, and npj Cardiovascular Health. Contact: jiarong.chen@sjtu.edu.cn
<a href='https://scholar.google.com/citations?user=40KXmRMAAAAJ'><img src="https://img.shields.io/endpoint?url={{ url | url_encode }}&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.

# 🔥 News
- *2026.07*: &nbsp;🎉🎉 <strong>Soft, Multi-Wavelength Photoplethysmography Enables Reliable Neonatal Blood Pressure Monitoring via Error Stratification</strong> is accepted by Advanced Science.
- *2026.07*: &nbsp;🎉🎉 <strong>A Multi-posture Asymmetry-aware Intelligent Bilateral Observation Dataset for Cardiovascular Monitoring</strong> is accepted by Scientific Data.
- *2026.07*: &nbsp;🎉🎉 <strong>Large-scale bilateral cardiovascular monitoring via wearable rings</strong> is accepted by npj Digitial Medicine.
- *2026.01*: &nbsp;🎉🎉 <strong>A Smart Ring for Long-Term Blood Pressure Monitoring </strong> has been accepted for Lecture presentation at the 2026 IEEE International Symposium on Circuits and Systems. (Date of Conference: 24-28 May 2026)
- *2025.08*: &nbsp;🎉🎉 <strong>Automated Pediatric Delirium Recognition via Deep Learning-Powered Video Analysis </strong> is accepted by IEEE Journal of Biomedical and Health Informatics.
- *2024.11*: &nbsp;🎉🎉 <strong>Joint HW/SW Signal Co-conditioning Strategy for Unobtrusive Single-Arm Cardiac Surveillance</strong> is accepted by EEE Transactions on Instrumentation and Measurement.
- *2024.11*: &nbsp;🎉🎉 <strong>Multi-Channel Masked Autoencoder and Comprehensive Evaluations for Reconstructing 12-Lead ECG from Arbitrary Single-Lead ECG</strong> is accepted by npj Cardiovascular Health.
- *2024.04*: &nbsp;🎉🎉 <strong>Conditional generative adversarial network driven variable-duration single-lead to 12-lead electrocardiogram reconstruction </strong> is accepted by Biomedical Signal Processing and Control.
- *2024.02*: &nbsp;🎉🎉 <strong>Implementing the confidence constraint cloud-edge collaborative computing strategy for ultra-efficient arrhythmia monitoring</strong> is accepted by Applied Soft Computing.
- *2023.04*: &nbsp;🎉🎉 <strong>Implementing ultra-lightweight co-inference model in ubiquitous edge device for atrial fibrillation detection </strong> is accepted by Expert Systems with Applications.
- *2022.05*: &nbsp;🎉🎉 <strong>Edge2Analysis: a novel AIoT platform for atrial fibrillation recognition and detection</strong> is accepted by  IEEE Journal of Biomedical and Health Informatics.

# 📝 Publications

<span style="font-size: 0.95em;">
† Equal contribution &nbsp;&nbsp; | &nbsp;&nbsp; * Corresponding author
</span>

## 2026

**[13] Soft, Multi-Wavelength Photoplethysmography Enables Reliable Neonatal Blood Pressure Monitoring via Error Stratification**  
Shi W, Mi L, **Chen J**, et al.  
*Advanced Science*, 2026, e76775.  
[Paper](https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.76775) ·
[Code](https://github.com/CHENJIAR3/neonatal_monitoring) ·
[DOI](https://doi.org/10.1002/advs.76775)

---

**[12] A Multi-posture Asymmetry-aware Intelligent Bilateral Observation Dataset for Cardiovascular Monitoring**  
**Chen J**, Li R, Liu B, et al.  
*Scientific Data*, 2026.  
[Paper](https://www.nature.com/articles/s41597-026-07915-8) ·
[Code](https://github.com/CHENJIAR3/MAIBO) ·
[DOI](https://doi.org/10.1038/s41597-026-07915-8)

---

**[11] Large-scale Bilateral Cardiovascular Monitoring via Wearable Rings**  
**Chen J**, Liu B, Shi W, Wang M, Gao R, Wang G, Chen C.  
*npj Digital Medicine*, 2026.  
[Paper](https://www.nature.com/articles/s41746-026-03036-z) ·
[Code](https://github.com/CHENJIAR3/BiPPG) ·
[DOI](https://doi.org/10.1038/s41746-026-03036-z)

---

**[10] A Smart Ring for Long-term Blood Pressure Monitoring**  
**Chen J**, Wang M, Liu B, Chen C, Wang G.  
In: *2026 IEEE International Symposium on Circuits and Systems (ISCAS)*,  
Shanghai, China, 2026, pp. 3955–3959.  
[Paper](https://ieeexplore.ieee.org/document/11562072) ·
[DOI](https://doi.org/10.1109/ISCAS66217.2026.11562072)


## 2025

**[9] Ring-BP: Using a Wearable Smart Ring to Cufflessly Estimate Blood Pressure with Mobile and Efficient Net**  
Liu B, Wu H, Wang G, **Chen J**, et al.  
In: *2025 IEEE 7th International Conference on Artificial Intelligence Circuits and Systems (AICAS)*,  
2025, pp. 1–5.  
[Paper](https://ieeexplore.ieee.org/document/11173101)

---

**[8] Development of a Rotation-Robust PPG Sensor for a Smart Ring**  
Wang M, Shi W, Zhang J, **Chen J**, et al.  
*Sensors*, 2025, 25(20): 6326.  
[Paper](https://www.mdpi.com/1424-8220/25/20/6326) ·
[DOI](https://doi.org/10.3390/s25206326)

---

**[7] Automated Pediatric Delirium Recognition via Deep Learning-Powered Video Analysis**  
**Chen J**, Xia S, Shi W, et al.  
*IEEE Journal of Biomedical and Health Informatics*, 2025.  
[Paper](https://ieeexplore.ieee.org/document/11145800) ·
[Code](https://github.com/CHENJIAR3/delirium_classification)
[DOI](10.1109/JBHI.2025.3604448)

## 2024

**[6] Joint HW/SW Signal Co-conditioning Strategy for Unobtrusive Single-Arm Cardiac Surveillance**  
Huang L, **Chen J**, Zhang X, et al.  
*IEEE Transactions on Instrumentation and Measurement*, 2024.  
[Paper](https://ieeexplore.ieee.org/document/10815987) ·
[Code](https://github.com/CHENJIAR3/ECG_Denoising/tree/Linfei) ·
[DOI](https://doi.org/10.1109/TIM.2024.3522425)

---

**[5] Multi-channel Masked Autoencoder and Comprehensive Evaluations for Reconstructing 12-lead ECG from Arbitrary Single-lead ECG**  
**Chen J**, Wu W, Liu T, et al.  
*npj Cardiovascular Health*, 2024, 1: 36.  
[Paper](https://www.nature.com/articles/s44325-024-00036-4) ·
[Code](https://github.com/CHENJIAR3/MCMA) ·
[DOI](https://doi.org/10.1038/s44325-024-00036-4)

---

**[4] Conditional Generative Adversarial Network-Driven Variable-Duration Single-Lead to 12-Lead Electrocardiogram Reconstruction**  
Zhan Z†, **Chen J†**, Li K, et al.  
*Biomedical Signal Processing and Control*, 2024, 95: 106377.  
[Paper](https://www.sciencedirect.com/science/article/pii/S174680942400435X) ·
[Code](https://github.com/Zehui-Zhan/12-lead-reconstruction) ·
[DOI](https://doi.org/10.1016/j.bspc.2024.106377)

---

**[3] Implementing the Confidence Constraint Cloud-Edge Collaborative Computing Strategy for Ultra-efficient Arrhythmia Monitoring**  
**Chen J**, Zhang X, Xu L, et al.  
*Applied Soft Computing*, 2024, 156: 111402.  
[Paper](https://www.sciencedirect.com/science/article/pii/S1568494624001765) ·
[DOI](https://doi.org/10.1016/j.asoc.2024.111402)


## 2023

**[2] Implementing Ultra-lightweight Co-inference Model in Ubiquitous Edge Device for Atrial Fibrillation Detection**  
**Chen J**, Jiang M, Zhang X, et al.  
*Expert Systems with Applications*, 2023, 216: 119407.  
[Paper](https://www.sciencedirect.com/science/article/pii/S0957417422024265) ·
[DOI](https://doi.org/10.1016/j.eswa.2022.119407)


## 2022

**[1] Edge2Analysis: A Novel AIoT Platform for Atrial Fibrillation Recognition and Detection**  
**Chen J**, Zheng Y, Liang Y, et al.  
*IEEE Journal of Biomedical and Health Informatics*, 2022, 26(12): 5772–5782.  
[Paper](https://ieeexplore.ieee.org/document/9769989) ·
[DOI](https://doi.org/10.1109/JBHI.2022.3172961)

# 📝 Academic Service

I have served as a peer reviewer for **100 manuscripts across 13 journals**, contributing to the peer-review process in biomedical engineering, wearable sensing, artificial intelligence, and healthcare.

### Peer Review

- *Biomedical Signal Processing and Control* 
- *Engineering Applications of Artificial Intelligence**
- *IEEE Journal of Biomedical and Health Informatics* 
- *IEEE Sensors Letters* 
- *IEEE Transactions on Consumer Electronics*
- *IEEE Internet of Things Journal* 
- *Information Sciences* 
- *Microelectronics* 
- *Pattern Recognition* 
- *IEEE Transactions on Knowledge and Data Engineering*
- *Intelligence-Based Medicine* 
- *International Journal of Cardiology* 
- *Neural Networks*

### Conference
- *IEEE BIOCAS 2026*
- *IEEE BIOCAS 2025*
 

# 🎖 Honors and Awards
<table border="1">
  <tr>
    <th>Date</th>
    <th>Achievement</th>
  </tr>
      <td style="text-align: left;">2025.11</td>
    <td style="text-align: left;">Awarded Excellent Paper in the PhD Student Academic Forum of Fudan University</td>
  <tr>
    <td style="text-align: left;">2024.07</td>
    <td style="text-align: left;">Outstanding Graduate, Sun Yat-sen University</td>
  </tr>
  <tr>
    <td style="text-align: left;">2023.10</td>
    <td style="text-align: left;">National Scholarship</td>
  </tr>
  <tr>
    <td style="text-align: left;">2023.09</td>
    <td style="text-align: left;">First-Class Scholarship for Outstanding Students, Sun Yat-sen University</td>
  </tr>
  <tr>
    <td style="text-align: left;">2023.07</td>
    <td style="text-align: left;">Third Prize, 8th National Biomedical Engineering Innovation Design Competition</td>
  </tr>
  <tr>
    <td style="text-align: left;">2022.09</td>
    <td style="text-align: left;">National Scholarship</td>
  </tr>
  <tr>
    <td style="text-align: left;">2022.09</td>
    <td style="text-align: left;">Samsung Scholarship</td>
  </tr>
  <tr>
    <td style="text-align: left;">2022.09</td>
    <td style="text-align: left;">First-Class Scholarship for Outstanding Students, Sun Yat-sen University</td>
  </tr>
  <tr>
    <td style="text-align: left;">2022.05</td>
    <td style="text-align: left;">Third Prize in 1st Guangdong Provincial Biomedical Engineering Innovation Design Competition</td>
  </tr>
  <tr>
    <td style="text-align: left;">2021.09</td>
    <td style="text-align: left;">Guangda Scholarship in Sun Yat-sen University</td>
  </tr>
  <tr>
    <td style="text-align: left;">2021.09</td>
    <td style="text-align: left;">First-Class Scholarship for Outstanding Students, Sun Yat-sen University</td>
  </tr>
  <tr>
    <td style="text-align: left;">2020.12</td>
    <td style="text-align: left;">First-Class Scholarship for Outstanding Students (Undergraduate), Sun Yat-sen University</td>
  </tr>
  <tr>
    <td style="text-align: left;">2019.11</td>
    <td style="text-align: left;">First Prize, 11th National College Mathematics Competition (Non-Mathematics Category)</td>
  </tr>
</table>

# 📖 Educations
- *2024.09 - now*, School of Electronic Information and Electrical Engineering,  Shanghai Jiao Tong University(Advisor: Prof Guoxing Wang)
- *2021.09 - 2024.06*, School of Biomedical Engineering, Sun Yat-sen University (Advisor: Prof Wanqing Wu)
- *2017.09 - 2021.06*, School of Biomedical Engineering, Sun Yat-sen University 

# 💻 Internships
- *2024.07 - 2024.09*, RingConn, ShenZhen, China.
- *2023.11 - 2024.04*, Peking University, Beijing, China.
