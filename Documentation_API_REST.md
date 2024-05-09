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

### RECUPERER TOUTES LES COMPAGNIES LIEES A UN UTILISATEUR 

    **GET** https://www.api.tanaguru.com/v1.0/service/auditPage

**Format de la requête**

    Headers 
    Authorization: bearer eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI.oGxndCq3Ocz6CKi2aUb4uA
    Accept: application/json; charset=utf-8
    Content-Type: application/json
    
    Payload
    {
    "page_url": "",
    "referentiel ": "", 
    "level ": "", 
    "language": "", 
    "dt_tbl_marker": "" ,
    "cplx_tbl_marker": "",
    "pr_tbl_marker": "", 
    "dcr_img_marker": "", 
    "inf_img_marker": "",
    "screen_width ": 1920, 
    "screen_height": 1080,
    "description_ref": true,
    "html_tags": false
    }

**Paramètres**

**Nom**			| **Requis**| **Type** 	| **Valeur par défaut**	| **Description**																| **Valeur possible**
----------------|-----------|-----------|-----------------------|-------------------------------------------------------------------------------|----------------------
Authorization	| Oui 		| String	| Aucune 				| Jeton d'authentification utilisé 												| bearer <valeur de jeton>
page_url 		| Oui 		| String	| Aucune 				| URL de la page à auditer 														| http://www. …..
referentiel 	| Non 		| String	| RGAA30 				| Le référentiel d’accessibilité à utiliser										| RGAA32016, RGAA30, RGAA22, AW22
level 			| Non 		| String	| AA 					| Le niveau d’accessibilité à utiliser 											| A, AA, AAA, Bz, Or, Ar, LEVEL_1, LEVEL_2, LEVEL_3
language		| Non 		| String	| All					| La langue des messages et les remarques de résultat d’audit					| All, Fr, En, Es_En, Es_Fr
dt_tbl_marker	| Non 		| String	| Aucune				| Marqueur HTML des tableaux de données											| Correspond à l'attribut "id", "class" ou "role" des tableaux complexes. Plusieurs marqueurs peuvent être saisis, séparées par un ;
cplx_tbl_marker	| Non 		| String	| Aucune				| Marqueur HTML des tableaux complexes											| Correspond à l'attribut "id", "class" ou "role" des tableaux complexes. Plusieurs marqueurs peuvent être saisis, séparées par un ;
pr_tbl_marker	| Non 		| String	| Aucune				| Marqueur HTML des tableaux de présentation 									| Correspond à l'attribut "id", "class" ou "role" des tableaux complexes. Plusieurs marqueurs peuvent être saisis, séparées par un ;
dcr_img_marker	| Non 		| String	| Aucune				| Marqueur des images décoratives												| Correspond à l'attribut "id", "class" ou "role" des tableaux complexes. Plusieurs marqueurs peuvent être saisis, séparées par un ;
inf_img_marker	| Non 		| String	| Aucune				| Marqueur des images porteuses d'informations									| Correspond à l'attribut "id", "class" ou "role" des tableaux complexes. Plusieurs marqueurs peuvent être saisis, séparées par un ;
screen_width	| Non 		| Number	| 1920					| Largeur de l’écran en pixel 													| Valeur maximum est 2048
screen_height	| Non 		| Number	| 1080					| Hauteur de l’écran en pixel													| Valeur maximum est 2048
description_ref	| Non 		| Boolean	| False					| Pour fournir ou non les intitulés des tests, critères, thème du référentiel. 	| True/False
html_tags		| Non 		| Boolean	| False					| Pour fournir les remarques et les intitulés encodé en htm ou non 				| True/False

**Format de la réponse**

    {
    "http_status_code": 200,
    "url": "",
    "status": "COMPLETED",
    "score": 100,
    "ref": "",
    "level": "",
    "language": "All",
    "nb_w3c_invalidated": 0,
    "nb_passed": 0,
    "nb_failed": 0,
    "nb_not_tested": 0,
    "nb_na": 0,
    "nb_failed_occurences": 0,
    "nb_detected": 0,
    "nb_suspected": 0,
    "nb_nmi": 0,
    "themes_description_en": {
    "Rgaa30-13": "…",
     …
      },
        
    	"themes_description_fr": {
        "Rgaa30-13": "…",
         …
      },
    "themes_description_es": {
        "Rgaa30-13": "…",
         …
      },
      "criterions_description_en": {
        "Rgaa30-12-11": "…",
       …
      },
      "criterions_description_fr": {
        "Rgaa30-12-11": "…",
       …
      },
      "tests_description_en": {
        "Rgaa30-11-1-2":"…",
        …
      },
      "tests_description_fr": {
        "Rgaa30-11-1-2":"…",
        …
      }, 
     "test_na": [
        {
          "criterion": "…",
          "test": "…",
          "theme": "…"
        },
        {…}
       ],
      "test_passed": [
        {
          "criterion": "…",
          "test": "…",
          "theme": "…"
        },
        {…}
       ],
      "remarks": [
        {
          "criterion": "",      
          "theme": "",
          "test": "",
          "issue": "",
          "message_en": "",
          "message_fr": "",
          "message_es": "",
          "line_number": 0,
          "snippet": ""
        }, 
        {…….}
      ]
    }

**Objet**

**Nom**						| **Type**	| **Description** 
----------------------------|-----------|-------------------
http_status_code			| Number	| Code retour du statut de la requête
url							| String	| URL auditée 
status						| String	| Status de l’audit 
score						| Number	| Score de l’audit en %
ref							| String	| Le référentiel utilisé pour l’audit 
level						| String	| Le niveau d’accessibilité utilisé pour l’audit 
language					| String	| La langue des messages et les remarques de résultat d’audit
nb_w3c_invalidated			| Number	| Nombre des erreurs w3c
nb_passed					| Number	| Nombre de teste validé
nb_failed					| Number	| Nombre de teste invalidé 
nb_not_tested				| Number	| Nombre de teste non testé
nb_na						| Number	| Nombre de teste non applicable 
nb_failed_occurences		| Number	| Nombre d’occurrence de testes invalidé
nb_detected					| Number	| A voir (Suppression de cette valeur) toujours zéro
nb_suspected				| Number	| A voir (Suppression de cette valeur) toujours zéro
nb_nmi						| Number	| Nombre de teste de pré-qualifié 
themes_description_en		| Objet		| Description des thèmes en anglais
themes_description_fr		| Objet		| Description des thèmes en français
themes_description_es		| Objet		| Description des thèmes en espagnole
criterions_description_en	| Objet		| Description des critères en anglais
criterions_description_fr	| Objet		| Description des critères en français
tests_description_en		| Objet		| Description des tests en anglais
tests_description_fr		| Objet		| Description des tests en français
test_na						| Array		| Vecteur contient tous les tests non applicable
test_passed					| Array		| Vecteur contient tous les tests validés 
remarks						| Array		| Vecteur contient tous les remarques de l’audit
criterion					| String	| Code du critère (la description à chercher dans criterions_description_en pour l’anglais et criterions_description_fr pour le français)  
theme						| String	| Code de la Thématique (la description à chercher dans themes_description_en pour l’anglais et themes_description_fr pour le français, themes_description_es pour l’espagnole)  
test						| String	| Code du test (la description à chercher dans tests_description_en pour l’anglais et tests_description_fr pour le français)  
issue						| String	| Code de la remarque
message_en					| String	| Description de la remarque en anglais 
message_fr					| String	| Description de la remarque en français
message_es					| String	| Description de la remarque en espagnole
line_number					| Number	| Nombre de ligne du code audité
snippet						| String	| Le bout de code HTML concerné par la remarque

**Exemple Curl**

    curl --ssl-reqd -H " Authorization: bearer eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI.oGxndCq3Ocz6CKi2aUb4uA"  -H "Accept: application/json; charset=utf-8" -H "Content-Type: application/json" -X POST -d ' {"page_url": "http://www.oceaneconsulting.com", "language":"all", "dt_tbl_marker":"data", "cplx_tbl_marker":"complexe", "pr_tbl_marker":"presentation", "dcr_img_marker":"decorative", "inf_img_marker":"informative"}' https://www.api.tanaguru.com/v1.0/service/auditPage
	
### STATISTIQUE D’UTILISATION DE L’API

	GET   https://www.api.tanaguru.com/v1.0/service/limit_stat

**Format de la requête**

	Headers 
	Authorization: bearer eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI.oGxndCq3Ocz6CKi2aUb4uA
	Accept: application/json; charset=utf-8
	Content-type: application/json

**Paramètres**

**Nom**	Authorization	
**Requis**	Oui
**Type**	String	
**Valeur par défaut**	Aucune
**Description**	Jeton d'authentification utilisé
**Valeur possible**	bearer <valeur de jeton>

**Format de la réponse**

	{
	"status" : 200, 
	"quotas_limit" : 0, 
	"quotas_used": 0, 
	"number_call": 0,
	"number_call_error": 0
	}

**Objet**

**Nom**				| **Type**	| **Description** 
--------------------|-----------|-------------------
status				| Number	| Code retour du statut de la requête
quotas_limit		| Number	| Limitation de quotas (nombre d’appels autorisé)
quotas_used			| Number	| Nombre d’appels effectué avec sucée
number_call			| Number	| Nombre d’appels effectué avec ou sans erreur
number_call_error	| Number	| Nombre d’appels retourné avec une erreur 

**Exemple Curl**

	curl --ssl-reqd -H " Authorization: bearer eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI.oGxndCq3Ocz6CKi2aUb4uA" -H "Accept: application/json; charset=utf-8" -H "Content-Type: application/json" -X GET
	https://www.api.tanaguru.com/v1.0/service/limit_stat

### DEMANDER UN JETON (AUTHENTIFICATION)

	POST   https://www.api.tanaguru.com/v1.0/security/authenticate

**Format de la requête**

	Headers 
	Authorization: basic YjkwMjVjNTZiMjQyNTA1M2RjMDYMmM3ZWI3M2QyMTA2NzY5NQ==
	Content-Type: application/json
	Grant_type: client_credentials

**Paramètres**

**Nom**	Authorization	
**Requis**	Oui
**Type**	String	
**Valeur par défaut**	Aucune
**Description**	Informations d'authentification
**Valeur possible**	basic <concaténation des clés et code secret de client encodé en Base64>

**Format de la réponse**

	{
	"status ": 200,
	"token_type": "bearer”,
	"access_token": ""
	}

**Objet**

**Nom**		| **Type**	| **Description** 
------------|-----------|-------------------
status		| Number	| Code retour du statut de la requête
token_type	| String	| Type de jeton
access_token| String	| Jeton d’authentification 

**Exemple Curl**

	curl --ssl-reqd -H " Authorization: basic YjkwMjVjNTZiMjQyNTA1M2RjMDYMmM3ZWI3M2QyMTA2NzY5NQ==" -H "Content-Type: application/json" -H "Grant_type: client_credentials" -X POST
	https://www.api.tanaguru.com/v1.0/service/security/authenticate

### INVALIDER UN JETON (AUTHENTIFICATION)

	POST   https://www.api.tanaguru.com/v1.0/security/invalidate_token

**Format de la requête**

	Headers 
	Authorization: basic YjkwMjVjNTZiMjQyNTA1M2RjMDYMmM3ZWI3M2QyMTA2NzY5NQ==
	Content-Type: application/json
	access_token: …

**Paramètres**

**Nom**			| **Requis**| **Type**	| **Valeur par défaut**	| **Description**						| **Valeur possible**
----------------|-----------|-----------|-----------------------|---------------------------------------|-------------------
Authorization	| Oui		| String	| Aucune				| Informations d'authentification		| basic <concaténation des clés et code secret de client encodé en Base64>
access_token	| Oui 		| String	| Aucune				| Jeton d’authentification à invalider	| Valeur de jeton

**Format de la réponse**

	{
	"status ": 200,
	"access_token": ""
	}

**Objet**

**Nom**			| **Type**	| **Description**
----------------|-----------|-------------------
status			| Number	| Code retour du statut de la requête
access_token	| String	| Jeton d’authentification qui a été invalidé 

**Exemple Curl**

	curl --ssl-reqd -H " Authorization: bearer eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI.oGxndCq3Ocz6CKi2aUb4uA" -H "Content-Type: application/json" -H "access_token:" -X POST
	https://www.api.tanaguru.com/v1.0/service/security/invalidate_token

## CAS D’ERREURS 

Cette section décrit quelques erreurs communes impliquées dans l'utilisation de jetons. Sachez que toutes les réponses d'erreur possibles ne sont pas couvertes ici ! 

**Obtenir un jeton avec une demande non valide (en laissant de côté Grant_type : client_credentials)**

	{
	"message": "grant_type value is missing",
	"status": 412
	}

**Obtenir un jeton avec une demande non valide (en laissant de côté Authorization)**

	{
	"message": "Consumer key & Consumer secret value are missing",
	"status": 412
	}

**Obtenir ou invalider un jeton avec des informations d'identification d'applications incorrectes ou périmées**

	{
	"message": "Unable to verify your credentials",
	"status": 403
	}

**Invalider un jeton incorrect ou périmé**

	{
	"message": "Invalid or expired token",
	"status": 403
	}

## GUIDE DE DEMARRAGE RAPIDE

### INSTALLATION D’UNE EXTENSION CHROME 

Depuis un navigateur chrome, rendez-vous à : https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo 

Lancer l’extension une fois installée. 

### DEMANDE DE JETON

	En supposant que votre ID BETA est : **b9025c56b2425053dc069585390ab7c8** et votre code secret BETA est : **10ee8cf96f9e35f7207a9a5cb3f89ed63c5f59692e1782d82c7eb73d21067695**. 
	
	**Remarque** : Pour la première version BETA de l'API Tanaguru, nous autorisons 5000 requêtes gratuite.

**Remarque** : Les informations d’authentification mentionnée sont seulement pour la version BETA, c’est juste un exemple. Rapprochez-vous de l'équipe Tanaguru pour avoir un ID client et un code secret valide (contact@tanaguru.com). 

1. Saisissez l’url pour l’authentification : **https://api.tanaguru.com/v1.0/service/security/authenticate** 
2. Choisissez la méthode de la requête **POST**  
3. Allez à l’onglet **Headers form** 
4. Ajoutez le paramètre **Authorization** 
5. Cliquez sur l’icône éditer la valeur du paramètre **Authorization**
6. Saisissez votre **ID Client** comme User name et **le code secret** comme Password, et validez.
7. Ajoutez le paramètre **Grant_type** et lui donner comme valeur **client_credentials** 
8. Ajoutez le paramètre **Content-type** et lui donner comme valeur **application/json**
9. Après avoir saisi toutes ces informations, cliquez sur **envoyer** pour faire la demande. 

![Capture d'écran d'une requette, étape ci-dessus](https://raw.githubusercontent.com/Tanaguru/Doc-API-REST/master/assets/capture01.png)

Vous obtiendrez la réponse ci-dessous : 

![Capture d'écran d'une réponse, étape ci-dessous](https://raw.githubusercontent.com/Tanaguru/Doc-API-REST/master/assets/capture02.png)

1. La réponse contient des informations à propos du **statut** de la réponse, ainsi que le type de **jeton** 
2. La valeur du **jeton** que vous allez utiliser ensuite pour faire des demandes d’audit. 

### INVALIDER UN JETON

Après avoir utilisé le jeton, si vous souhaitez l’invalider pour une raison quelconque,

1. Saisir l’url pour l’authentification : **https://api.tanaguru.com/v1.0/service/security/invalidate_token**
2. Vous devrez faire une demande **POST**, 
3. Allez à l’onglet **Headers form** 
4. Ajoutez le paramètre **Authorization**, 
5. Cliquez sur l’icône éditer la valeur du paramètre **Authorization**
6. Saisissez votre **ID Client** comme User name et le **code secret** comme Password, et validez.
7. Ajoutez le paramètre **Accept** et lui donner comme valeur **application/json ; charset=utf-8** 
8. Ajoutez le paramètre **Content-type** et lui donner comme valeur **application/json**
9. Ajoutez le paramètre **access_token** et saisissez le jeton que vous voulez invalider. 
10. Cliquez sur **Envoyer** pour faire la demande.	

![Capture d'écran d'une requette, étape ci-dessus](https://raw.githubusercontent.com/Tanaguru/Doc-API-REST/master/assets/capture03.png)

### LANCER UN AUDIT DE PAGE

Pour lancer un audit sur le site http://www.oceaneconsulting.com avec toutes les langues,

1. Saisir l’url pour l’authentification : **https://api.tanaguru.com/v1.0/service/auditPage**
2. Faites une demande **POST**, 
3. Choisissez **application/json** comme type de donnée à envoyer. 
4. Allez à l’onglet **Headers form** 
5. Ajoutez le paramètre **Authorization**
6. Utilisez le type de jeton **bearer** concaténé avec votre **jeton** comme : **bearer eyJH...** 
7. Ajoutez le paramètre **Accept** et lui donner comme valeur */*
8. Ajoutez le paramètre **Content-type** et lui donner comme valeur **application/json**
9. Allez à l’onglet **Raw payload** 
10. Vous saisissez en format Json {**"page_url" : "http://www.oceaneconsulting.com"}**, vous n’êtes pas obligé de rajouter les attributs **language, referentiel et level** parce qu’ils ont des valeurs par default (All, Rgaa30, AA). 
11. Cliquez sur **envoyer** pour faire la demande.

![Capture d'écran d'une requette, étape ci-dessus](https://raw.githubusercontent.com/Tanaguru/Doc-API-REST/master/assets/capture04.png)

### STATISTIQUE D’UTILISATION DE L’API 

Pour connaître les statistiques d’utilisation de l’API avec votre compte 

1. Saisir l’url pour l’authentification : **https://api.tanaguru.com/v1.0/service/limit_stat**
2. Faites une demande **GET**
3. Allez à l’onglet **Headers form** 
4. Ajoutez le paramètre **Authorization**
5. Utilisez le type de jeton **bearer** concaténé avec votre jeton comme : **bearer eyJH...** 
6. Ajoutez le paramètre **Accept** et lui donner comme valeur **application/json ; charset=utf-8**
7. Ajoutez le paramètre **Content-type** et lui donner comme valeur **application/json**
8. Cliquez sur **envoyez** pour faire la demande.	
9. La réponse contient des informations d’utilisation de l’api.  

![Capture d'écran d'une requette, étape ci-dessus](https://raw.githubusercontent.com/Tanaguru/Doc-API-REST/master/assets/capture05.png)

