---
materia: Algoritmi e Strutture Dati
argomento: Tabelle Hash
tipo: struttura-dati
esame_anno: 2026/2027
stato: revisionato
tags:
  - asd
  - strutture-dati
  - complessità
---

# Tabelle Hash con Risoluzione per Concatenamento (Chaining)

> [!abstract] Concetto Chiave
> Struttura dati che implementa un dizionario associando chiavi a valori tramite una funzione hash $h(k)$. I conflitti tra chiavi aventi lo stesso hash vengono risolti allocando gli elementi in liste concatenate collegate ai bucket dell'array.

---

### Formalizzazione Matematica
Data una tabella $T$ di dimensione $m$ e $n$ elementi memorizzati:
* **Fattore di carico:** $\alpha = \frac{n}{m}$ (rappresenta la lunghezza media di ogni catena).
* **Funzione hash ideale:** Ipotesi di *Simple Uniform Hashing*, dove ogni elemento ha probabilità uniforme $\frac{1}{m}$ di cadere in uno qualsiasi degli $m$ bucket, indipendentemente dalla destinazione degli altri.

---

### Analisi della Complessità

| Operazione | Caso Migliore | Caso Medio (SUH) | Caso Pessimo (Collisioni totali) |
|---|---|---|---|
| **Inserimento** | $O(1)$ (in testa) | $O(1)$ | $O(1)$ (in testa) / $O(n)$ (in coda con deduplicazione) |
| **Ricerca** | $O(1)$ | $\Theta(1 + \alpha)$ | $\Theta(n)$ |
| **Cancellazione** | $O(1)$ | $O(1)$ (con lista doppiamente linkata) | $\Theta(n)$ (con lista singolarmente linkata) |

---

### Implementazione Minimale (Pseudocodice / C)

```c
typedef struct Node {
    int key;
    int value;
    struct Node* next;
} Node;

typedef struct HashTable {
    int size;
    Node** buckets; // array di puntatori a testa di lista
} HashTable;

// Inserimento O(1) in testa alla lista del bucket calcolato
void insert(HashTable* table, int key, int val) {
    int index = hash(key) % table->size;
    Node* newNode = malloc(sizeof(Node));
    newNode->key = key;
    newNode->value = val;
    newNode->next = table->buckets[index];
    table->buckets[index] = newNode;
}
```

---

### Trappole d'Esame & Domande Orale

* **Scelta della lista:** Perché si usa una lista doppiamente concatenata anziché singolarmente linkata?  
  *Risposta:* Per garantire la cancellazione in $O(1)$ quando si ha già il puntatore al nodo (eliminando il tempo di scansione per trovare il predecessore).
* **Degenerazione in lista:** Se $h(k)$ mappa tutte le chiavi sullo stesso bucket, le prestazioni collassano a quelle di una lista lineare ($\Theta(n)$ per la ricerca).

---

### Flashcard Anki

> [!question] Complessità Ricerca Hash Chaining
%%
START
Basic
In una tabella Hash con Chaining sotto l'ipotesi di Simple Uniform Hashing, qual è la complessità media di una ricerca con successo e insuccesso?
Back: 
In entrambi i casi è **$\Theta(1 + \alpha)$**, dove $\alpha = n/m$ è il fattore di carico.
- $1$ è il tempo di calcolo dell'hash $h(k)$ e accesso al bucket.
- $\alpha$ è il tempo medio di scansione della catena associata.
<!--ID: 1718902991001-->
END
%%

> [!question] Requisito per Cancellazione O(1) Hash Chaining
%%
START
Basic
Qual è il prerequisito strutturale per eseguire la cancellazione di un elemento da una tabella hash con chaining in $O(1)$?
Back:
La catena di trabocco deve essere implementata come **lista doppiamente concatenata** (e dobbiamo già avere il puntatore al nodo da rimuovere), per consentire lo sganciamento senza dover ricercare il puntatore precedente.
<!--ID: 1718902991002-->
END
%%



> [!question]- Flashcard: Race condition
> START
> Basic
> Cos'è una race condition?
> Back: [...]
> <!--ID: 1718902845126-->
> END