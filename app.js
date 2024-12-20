// Importa Firebase Admin SDK
var admin = require("firebase-admin");

// Ruta al archivo de credenciales JSON
var serviceAccount = require("./serviceAccountKey.json");  // Asegúrate de que la ruta sea correcta

// Inicializa la aplicación de Firebase
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

// Ahora puedes utilizar Firebase. Por ejemplo, accediendo a Firestore:
var db = admin.firestore();

// Ejemplo de consulta a la colección "users":
db.collection('users').get()
  .then(snapshot => {
    snapshot.forEach(doc => {
      console.log(doc.id, '=>', doc.data());
    });
  })
  .catch(err => {
    console.log('Error al obtener documentos:', err);
  });
