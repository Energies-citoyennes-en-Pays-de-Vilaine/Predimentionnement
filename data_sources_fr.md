# Eources de donnees et transformations

## Zones concernees

Il s'agit du CC Pontchateau et du CA Redon

## Periode concernee

Etant donne les sources de donnees actuelles, la periode concernee sont les annees 2020->2021 et 2021->2022

## eoliennes :

La courbe production eolienne fournie par ELFE d'une eolienne du site de Beganne. Afin de correspondre au parc existant, une mise a l'echelle est effectuee. Actuellement il s'agit d'une simple multiplication par le nombre d'eoliennes présentes sur le parc, il va probablement falloir mettre ces donnees a jour car les eolinnes installées ne font probablement pas toutes la meme puissance.

Cette puissance est alors consideree comme repartie equitablement entre tous les foyers des zones concernees, puis multipliee par 200. Lorsque la consommation des entreprises sera prise en compte, il faudra determiner quelle proportion le projet prevoit de leur attribuer, mais cela changera le facteur d'echelle.

## Production Solaire : 

Les donnees de production solaires utilisees sont actuellement celles founies par ENEDIS

Les donnees de production solaire sont connues a l'echelle de la demi-heure sur la region Bretagne sur la periode (2019-01-01 -> date d'export du fichier), mais seulement a l'echelle de l'annee jusqu'a l'annee 2020-2021 pour les zones geographiques concernees (CC Pontchateau et CA Redon). La courbe de production bretonne est normalisee (divisee par sa moyenne sur les periodes concernees) pour chacune des annees entieres disponnibles puis multipliee par la moyenne de production sur un an (l'annee de reference est actuellement l'annee 2020-2021 jusqu'a l'obtention de meilleures informations)

La repartition de cette production est effectuee similairement a celle eolienne

## Production Bioeneregetique

Les donnees de production Bioenergetiques utilisees sont actuellement celles founies par ENEDIS et sont traitees comme celle de production Solaire

## Consomation

Les donnes de consommation sont celles fournies par Enedis, on applique aux consommateurs le profil de consommation du resident Breton moyen et on genere actuellement 200 de ces consommateurs.
