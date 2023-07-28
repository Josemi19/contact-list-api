# Guia para usar el contact API

## ENDPOINTS

### 1. /contacts

1. Metodo 'GET':

   Devuelve un array de todos los contactos.
2. Metodo 'POST':

    Para **crear** un nuevo contacto. Es necesario enviar en el body un objeto con las siguientes propiedades.
   - email.
   - full_name.
   - phone_number.
   - adress.

```js
// EJEMPLO
fecth(`${TU_URL}/contacts`, {
  method: 'POST',
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "email": email,
    "full_name": full_name,
    "phone_number": phone_number,
    "adress": adress
  })
})
```
3. Metodo 'PUT':

   Para **actualizar** un contacto. Es necesario enviar **todos** los campos tal y como en el metodo 'POST', tanto los que quieren actualizar como los que no.

```js
// EJEMPLO
fecth(`${TU_URL}/contacts`, {
  method: 'PUT',
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "email": email,
    "full_name": full_name,
    "phone_number": phone_number,
    "adress": adress
  })
})
```
4. Metodo 'DELETE":

   Para **borrar** un contacto. Es necesario enviar en el body **solo** el 'id' del contacto.

```js
// EJEMPLO
fecth(`${TU_URL}/contacts`, {
  method: 'DELETE',
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "id": id
  })
})
```
