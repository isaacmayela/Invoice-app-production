# DOCUMENTATION DE L’API REST INVOICE MANAGER V0.1

DOCUMENTATION Api Invoice Manager


## INTRODUCTION 

L’API REST fournit une API de services Web pratique, puissante, simple pour interagir avec l'application web invoice manager. Elle présente comme avantages une grande facilité d'intégration et de développement. C’est également une excellente solution pour une utilisation avec des applications mobiles et Web. 

L’utilisation de l'API exige une connaissance de base des services Web. 

URL de base de l'API : https://invoicemanagerbackend.onrender.com/

Tous les appels de l'API commencent par cette URL à laquelle s'ajoute le chemin vers l'action désirée. 

Exemple : https://invoicemanagerbackend.onrender.com/homePage 

L'API est accessible uniquement via le protocole Https et accepte les requêtes HTTP POST et GET. Les données envoyées en POST doivent respecter le format JSON.

## AUTHENTIFICATION 

L’API REST utilise l'authentification par token (json web token) en utilisant la bibliothèque Python django rest framework simplejwt pour permettre aux utilisateurs d'applications d'accéder en toute sécurité aux données sans avoir à révéler nom d'utilisateur et mot de passe.

Avant de procéder à des appels d'API REST, vous devez vous authentifier Pour ce faire, vous aurez besoin des éléments suivants : 

* Un Email et un mot de passe. 
* Faire une requête POST security/authenticate pour échanger ces informations d’identification et générer un jeton d’authentification via l’API. Ensuite pour toutes les requêtes, vous devez préciser dans le paramètre d’authentification sur le header de la requête, le jeton comme valeur.

![Shema d'authentification, description ci-dessous](https://app.diagrams.net/#G1chZxcNJX0x6OynhMsv38mSqwyHFRhb9_#%7B%22pageId%22%3A%22OktIcNigZE0he0N_YRCG%22%7D)

**Phase 1 : Autentification**

1. Faire une requête POST sur accounts/login en utilisant l'email et le mot de passe pour demander un jeton.
2. L’API reçoit la requête et génère un jeton et le renvoie au client sous format JSON.
3. Le client reçoit le jeton et le parse pour récupérer la valeur de jeton pour l’utiliser dans la phase 2.

**Phase 2 : Appels vers l’API**

1. Le client lance une requête POST sur /company/all_invoices/ avec la valeur de jeton comme un identifiant pour récupérer toutes les facture qu'il a crée.
2. L’API traite la requête et renvoie les données du résultat sous format JSON au client.
3. Le client reçoit les données et les parse pour des utilisations diverses. 


**Les jetons sont des mots de passe**

Gardez à l'esprit que l'email', le mot de passe et le jeton sont indispensables pour accéder aux demandes liées à une application. Ces valeurs doivent être considérées comme sensibles et ne doivent pas être partagées ou distribuées à des personnes non fiables. 

**SSL absolument nécessaire**

Cette authentification n’est fiable uniquement que si SSL est utilisé. Par conséquent, toutes les demandes pour obtenir et utiliser les jetons doivent utiliser des paramètres HTTPS, c’est également une exigence de l'API.

### ÉTAPE 1 : ENVOI DE L'EMAIL ET DU MOT DE PASSE DU CLIENT

Le client envoi son adrèsse mail et son mot de passe

### ÉTAPE 2 : OBTENIR UN JETON

Les données recues doivent être échangée contre un jeton en émettant une demande de POST /accounts/login :

* La demande doit être une requête HTTP POST.
* La demande doit inclure un en-tête Content-Type avec la valeur application/json.

Exemple de demande :

    POST /accounts/login HTTP/1.1
    Host: invoicemanagerbackend.onrender.com
    User-Agent: My App v1
    Authorization: Basic 
    Content-Type: application/json

Si la demande a été correctement formatée, le serveur répond avec un payload JSON codé :

Exemple de réponse :


    HTTP/1.1 200 OK
    Status: 200 OK
    Content-Type: application/json; charset=utf-8
    ...
    {‘’status’’: 200 ,’’token_type’’: ‘’bearer’’ , ‘’access’’: ‘’AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%2FAAAAAAAAAAAA’’, refresh: ‘’AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%2FAAAAAAAAAAAA’’}

Les demandes doivent vérifier que la valeur associée à la clé token_type de l'objet retourné est « **bearer** ». Les valeur associées aux clés access et refresh sont les jetons.

Notez qu'un jeton d'accès à une durée de vie limitée de dix minutes, le client pourra utiliser le token de raffraichissement afin de raffraichir le token d'accès. 

### ÉTAPE 3 : AUTHENTIFIER LES REQUETES API AVEC LE JETON

Le jeton d'accès est utilisé pour faire des appels vers l’API. Pour utiliser le jeton d'accès, construire une demande HTTPS normale et inclure un en-tête **Authorization** avec la valeur du jeton : **Bearer < valeur de jeton de l'étape 2>**. La signature n’est pas nécessaire.

Exemple de demande : 

    GET /v1.0/company/all_invoices/ HTTP/1.1
    Host: invoicemanagerbackend.onrender.com
    User-Agent: My App v1.0
    Authorization: Bearer AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%2FAAAAAAAAAAAAAAA


## STATUT DU RETOUR, LISTE DES CODES

Chaque appel à l'API donne lieu à une réponse retournant un code spécifique en fonction du résultat obtenu. L'analyse de ce code vous permet de vous assurer que la requête a été traitée avec succès.

Tous les codes >= 400 indiquent que la requête n'a pas été traitée avec succès par nos serveurs.

* **200**: OK
* **400**: Paramètre manquant, ou valeur incorrecte
* **401**: Authentification nécessaire (jeton non précisé ou invalide)
* **403**: Action non autorisée (crédits épuisés, URL non autorisée, etc)
* **404**: Page inaccessible (URL inconnue / impossible d'accéder à l'adresse)
* **500**: Erreur interne au serveur

## LISTE DES ACTIONS DISPONIBLES
