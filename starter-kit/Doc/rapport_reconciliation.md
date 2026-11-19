# Rapport de réconciliation des numéros de TVA

## 1. Objectif

Résultats des contrôles sur les numéros de TVA du fichier initial.

L'objectif est de distinguer :

- Les numéros valides.
- Les numéros invalides.
- Les numéros non tranchés, pour lesquels une erreur technique empêche de conclure.

La vérification se déroule en deux étapes : un contrôle de la structure des numéros, puis une interrogation du service européen VIES sur un échantillon.

## 2. Résultats du contrôle structurel

Le fichier initial contient **10 000 numéros de TVA**.

Après nettoyage et vérification de leur structure :

- **6 083** numéros respectent les règles de validation structurelle.
- **281** doublons ont été identifiés.
- **5 802** numéros structurellement valides et uniques ont été conservés pour la suite du traitement.

Les numéros rejetés présentent notamment des erreurs de clé de contrôle, des pays non pris en charge ou des formats incorrects.

⚠️ Un numéro structurellement valide n'est pas nécessairement un numéro de TVA actif. C'est pourquoi une seconde vérification a été réalisée avec le service européen VIES.

## 3. Résultats de la vérification VIES

Un échantillon de **200 numéros de TVA** a été sélectionné parmi les 5 802 numéros structurellement valides et uniques.

Les numéros ont été vérifiés à l'aide de l'API européenne VIES.

| Résultat     |  Nombre | Pourcentage |
| ------------ | ------: | ----------: |
| Valides      |       8 |         4 % |
| Invalides    |     171 |      85,5 % |
| Non tranchés |      21 |      10,5 % |
| **Total**    | **200** |   **100 %** |

**Interprétation :**

- **Valide :** le service VIES confirme la validité du numéro.
- **Invalide :** le service VIES indique que le numéro n'est pas valide.
- **Non tranché :** une erreur technique ou un délai d'attente empêche de déterminer sa validité.

Les résultats non tranchés ne doivent pas être considérés comme invalides. Ils nécessitent une nouvelle vérification.

Ces résultats concernent uniquement l'échantillon testé et ne permettent pas de conclure directement sur l'ensemble des 5 802 numéros.

## 4. Difficultés rencontrées lors de la collecte VIES

- **Limitation des requêtes (`MS_MAX_CONCURRENT_REQ`) :** le service VIES a parfois refusé de traiter certaines demandes en raison d'un trop grand nombre de requêtes simultanées.
- **Dépassement du délai d'attente (`timeout`) :** certaines requêtes n'ont pas reçu de réponse dans les 10 secondes autorisées.
- **Gestion des réponses `VALID` :** une condition dans le script considérait initialement ces réponses comme des erreurs. Cette condition a été corrigée afin d'enregistrer les résultats valides.

Pour limiter ces problèmes, une pause de 10 secondes a été ajoutée entre les requêtes.

Le script enregistre également les informations dans un fichier journal (`collecte_vies.log`) et sauvegarde progressivement les résultats dans un fichier CSV.

Grâce à ce système, une collecte interrompue peut être relancée sans perdre les résultats déjà enregistrés.

## 5. Conclusion et recommandations

L'analyse a permis de nettoyer et de contrôler les numéros de TVA du fichier initial.

Sur les **10 000 numéros**, 5 802 numéros structurellement valides et uniques ont été conservés.

Un échantillon de 200 numéros a ensuite été interrogé avec le service VIES. Les résultats montrent que certains numéros respectent les règles de format sans être reconnus comme valides par VIES.

**Recommandations pour la direction financière :**

1. **Conserver les numéros confirmés valides** par VIES, en enregistrant la date de vérification.
2. **Faire vérifier les numéros invalides** avant leur utilisation dans les opérations comptables.
3. **Relancer les vérifications non tranchées**, car une erreur technique ne signifie pas que le numéro est invalide.
4. **Mettre en place des contrôles réguliers** pour maintenir la qualité des données.
