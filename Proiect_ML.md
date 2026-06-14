|     |     | Predictia |          | Complexit˘atii |        |              |          | Lexicale |     |     |
| --- | --- | --------- | -------- | -------------- | ------ | ------------ | -------- | -------- | --- | --- |
|     |     |           | ,        |                |        |              | ,        |          |     |     |
|     |     |           | din Date |                | de     | Eye-Tracking |          |          |     |     |
|     |     |           |          | Sugestii       | pentru |              | studenti |          |     |     |
,
Problema
Dat un cuvˆant dintr-un text romˆanesc, preziceti un scor de complexitate ˆın intervalul [0,1],
,
unde 0ˆınseamn˘a foarte familiar si 1ˆınseamn˘a foarte dificil. Semnalul principal de antrenareˆıl
,
reprezint˘a metricile de eye-tracking colectate de la participanti umaniˆın timpul citirii (durata
,
| fixatiilor, | num˘arul | de  | regresii, timpul | de  | recitire | etc). |     |     |     |     |
| ----------- | -------- | --- | ---------------- | --- | -------- | ----- | --- | --- | --- | --- |
,
Challenges
•
Putine exemple adnotate cu scoruri de complexitate: insuficient pentru orice model
,
| ML  | clasic | f˘ar˘a inginerie | atent˘a | a   | caracteristicilor. |     |     |     |     |     |
| --- | ------ | ---------------- | ------- | --- | ------------------ | --- | --- | --- | --- | --- |
•
Variabilitate inter-individual˘a: acelasi cuvˆant e citit diferit de fiecare participant;
,
| trebuie | agregate |     | aceste valori. |     |     |     |     |     |     |     |
| ------- | -------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
• Complexitatea e subiectiv˘a: depinde de cititorul individual, contextul propozitiei,
,
| domeniul |     | textului. |     |     |     |     |     |     |     |     |
| -------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
• Tokenizare inconsistent˘a: ˆımp˘artireaˆın cuvinte difer˘aˆıntre datele ET si cele de com-
|           |     |           |          |              | ,   |     |     |     | ,   |     |
| --------- | --- | --------- | -------- | ------------ | --- | --- | --- | --- | --- | --- |
| plexitate |     | (cratime, | semne de | punctuatie). |     |     |     |     |     |     |
,
• Leaderboard public ̸= leaderboard privat: un scor bun pe public nu garanteaz˘a
| generalizare |     | pe           | datele private. |     |     |     |     |     |     |     |
| ------------ | --- | ------------ | --------------- | --- | --- | --- | --- | --- | --- | --- |
| Features     | din | Eye-Tracking |                 |     |     |     |     |     |     |     |
•
Agregati metricile ET per cuvˆant (mean, std, median, max) peste toti participantii
|        | ,     |           |                 |     |      |           |           |     | ,   | ,   |
| ------ | ----- | --------- | --------------- | --- | ---- | --------- | --------- | --- | --- | --- |
| • Skip | rate: | proportia | participantilor |     | care | au s˘arit | cuvˆantul |     |     |     |
|        |       |           | ,               | ,   |      |           |           |     |     |     |
•
| Rapoarte |     | derivate: | RRT/FPRT, |     | TFC/lungime |     | cuvˆant |     |     |     |
| -------- | --- | --------- | --------- | --- | ----------- | --- | ------- | --- | --- | --- |
• Deviatia standard mareˆıntre participanti poate indica ambiguitate sau dificultate
|            | ,           |                |           |     |           | ,   |        |     |     |     |
| ---------- | ----------- | -------------- | --------- | --- | --------- | --- | ------ | --- | --- | --- |
| Features   | Lingvistice |                |           |     |           |     |        |     |     |     |
| • Lungimea |             | cuvˆantuluiˆın | caractere |     | si num˘ar | de  | silabe |     |     |     |
,
| • Frecventa |     | din corpus | romˆanesc | cu  |     |     |     |     |     |     |
| ----------- | --- | ---------- | --------- | --- | --- | --- | --- | --- | --- | --- |
wordfreq
,
• Este cuvˆant functional? (prepozitii, conjunctii → aproape mereu simple)
|             |     |         | ,        |         | ,        | ,   |     |     |     |     |
| ----------- | --- | ------- | -------- | ------- | -------- | --- | --- | --- | --- | --- |
| • Cuvintele |     | compuse | tind s˘a | fie mai | complexe |     |     |     |     |     |
1

ˆ
| Modele     | de Incercat |              |               |            |                |         |             |
| ---------- | ----------- | ------------ | ------------- | ---------- | -------------- | ------- | ----------- |
| • Ridge    | Regression  | cu           | leave-one-out |            | CV             |         |             |
| • Random   | Forest:     | ofer˘a       | feature       | importance |                |         |             |
| • XGBoost  | cu          | regularizare |               | mare       |                |         |             |
| • Romanian | BERT:       |              | embeddings    |            | per cuvˆantˆın | context | ca features |
• Surprisal dintr-un language model: cˆat de neasteptat e cuvˆantul respectivˆıntr-un context
,
dat
| Alte strategii |     | pentru | a extinde | setul | de  | antrenare: |     |
| -------------- | --- | ------ | --------- | ----- | --- | ---------- | --- |
• Transfer de adnot˘ari din alte limbi: exist˘a seturi de date de complexitate ˆın en-
glez˘a sau german˘a (ex. CWI Shared Task). Puteti antrena un model acolo si transfera
, ,
reprezent˘arileˆın romˆan˘a via embeddings multilinguale (mBERT, XLM-R)
• Morphological complexity: num˘ar de morfeme, lungime, num˘ar de silabe, prezenta
,
| sufixelor | rare | folosind | spaCy | sau | stanza | pentru romˆan˘a |     |
| --------- | ---- | -------- | ----- | --- | ------ | --------------- | --- |
• Zipf score: transformare standard a frecventei, direct disponibilˆın wordfreq
,
| • Readability |     | features: | Flesch-Kincaid |     |     |     |     |
| ------------- | --- | --------- | -------------- | --- | --- | --- | --- |
(https://www.geeksforgeeks.org/python/readability-index-pythonnlp/)
| adaptat | pentru | romˆan˘a, | bazat |     | pe silabe | si lungime |     |
| ------- | ------ | --------- | ----- | --- | --------- | ---------- | --- |
,
2