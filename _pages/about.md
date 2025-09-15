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
My name is Jiarong Chen. Currently, my research interests include generative artificial intelligence, digital health, AI for healthcare, bio-signal processing (mainly ECG and PPG), and cardiovascular health. I have published my research findings in several international journals, including IEEE Journal of Biomedical and Health Informatics, Expert Systems With Applications, Biomedical Signal Processing and Control, Applied Soft Computing, IEEE Transactions on Instrumentation and Measurement, and npj Cardiovascular Health. I am a peer-reviewer for some journals, including IEEE Journal of Biomedical and Health Informatics Biomedical Signal Processing and Control, Information Sciences, Enginnering Application of Artificial Intelligence. Contact: jiarong.chen@sjtu.edu.cn
<a href='https://scholar.google.com/citations?user=40KXmRMAAAAJ'><img src="https://img.shields.io/endpoint?url={{ url | url_encode }}&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>.

# 🔥 News
- *2025.08*: &nbsp;🎉🎉 <strong>Automated Pediatric Delirium Recognition via Deep Learning-Powered Video Analysis </strong> is accepted by IEEE JBHI.
- *2024.11*: &nbsp;🎉🎉 <strong>Joint HW/SW Signal Co-conditioning Strategy for Unobtrusive Single-Arm Cardiac Surveillance</strong> is accepted by IEEE TIM.
- *2024.11*: &nbsp;🎉🎉 <strong>Multi-Channel Masked Autoencoder and Comprehensive Evaluations for Reconstructing 12-Lead ECG from Arbitrary Single-Lead ECG</strong> is accepted by npj Cardiovascular Health.
- *2024.04*: &nbsp;🎉🎉 <strong>Conditional generative adversarial network driven variable-duration single-lead to 12-lead electrocardiogram reconstruction </strong> is accepted by BSPC.
- *2024.02*: &nbsp;🎉🎉 <strong>Implementing the confidence constraint cloud-edge collaborative computing strategy for ultra-efficient arrhythmia monitoring</strong> is accepted by ASoC.

# 📝 Publications 

<div class='paper-box'><div class='paper-box-image'><div><div class="badge"></div><img src='images/ASOC.png' alt="sym" style="width: 500px; height: auto;"></div></div>
<div class='paper-box-text' markdown="1">
<strong>**ECG Classification**</strong>
<br>
[1] **Chen J**, Jiang M, Zhang X, et al. Implementing ultra-lightweight co-inference model in ubiquitous edge device for atrial fibrillation detection[J]. Expert Systems with Applications, 2023, 216: 119407. (JCR Q1, IF=8.6)
[[Online]](https://www.sciencedirect.com/science/article/abs/pii/S0957417422024265)
<p></p>
[2] **Chen J**, Zheng Y, Liang Y, et al. Edge2Analysis: a novel AIoT platform for atrial fibrillation recognition and detection[J]. IEEE Journal of Biomedical and Health Informatics, 2022, 26(12): 5772-5782. 
[[Online]](https://ieeexplore.ieee.org/document/9769989)
<p></p>
[3] **Chen J**, Zhang X, Xu L, et al. Implementing the confidence constraint cloud-edge collaborative computing strategy for ultra-efficient arrhythmia monitoring[J]. Applied Soft Computing, 2024: 111402. (JCR Q1, IF=8.7)
[[Online]](https://www.sciencedirect.com/science/article/pii/S1568494624001765)

</div>
</div>
<div class='paper-box'><div class='paper-box-image'><div><div class="badge"></div><img src='images/12lead_ECG_reconstruction.png' alt="sym" style="width: 500px; height: auto;"></div></div>
<div class='paper-box-text' markdown="1">
<strong>**ECG Reconstruction**</strong>
<br>
[4] Zhan Z+, **Chen J+ (co-first author)**, Li K, et al. Conditional Generative Adversarial Network Driven Variable-Duration Single-Lead to 12-Lead Electrocardiogram Reconstruction[J]. Biomedical Signal Processing and Control, 2024, 95: 106377. (JCR Q1, IF=5.1)
[[Online]](https://www.sciencedirect.com/science/article/pii/S174680942400435X)
[[Code]](https://github.com/Zehui-Zhan/12-lead-reconstruction)
<p></p>
[5] **Chen J**, Wu W, Liu T, et al. Multi-channel masked autoencoder and comprehensive evaluations for reconstructing 12-lead ECG from arbitrary single-lead ECG[J]. npj Cardiovascular Health, 2024, 1(1): 1-13.
[[Online]](https://www.nature.com/articles/s44325-024-00036-4)
[[Code]](https://github.com/CHENJIAR3/MCMA)
<p></p>
[6] Huang L,**Chen J**, Zhang X, et al. Joint HW/SW Signal Co-conditioning Strategy for Unobtrusive Single-Arm Cardiac Surveillance[J]. IEEE Transactions on Instrumentation and Measurement, 2024: 1-1. DOI:10.1109/TIM.2024.3522425
[[Online]](https://ieeexplore.ieee.org/document/10815987)
[[Code]](https://github.com/CHENJIAR3/ECG_Denoising/tree/Linfei)
</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge"></div><img src='images/fig1_v2.png' alt="sym" style="width: 500px; height: auto;"></div></div>
<div class='paper-box-text' markdown="1">
<strong>**Pediatric Healthcare**</strong>
<br>
[7] Chen J, Xia S, Shi W, et al. Automated Pediatric Delirium Recognition via Deep Learning-Powered Video Analysis[J]. IEEE Journal of Biomedical and Health Informatics, 2025.
[[Online]](https://ieeexplore.ieee.org/document/11145800)
[[Code]](https://github.com/CHENJIAR3/delirium_classification)
</div>
</div>

# 🎖 Honors and Awards
<table border="1">
  <tr>
    <th>Date</th>
    <th>Achievement</th>
  </tr>
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
