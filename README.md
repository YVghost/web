# MarketCampus – Proyecto Web Django

## Descripción del Proyecto
MarketCampus es una aplicación web desarrollada con el framework Django que permite la gestión, exploración y compra de productos a través de un flujo de checkout básico. El proyecto fue refactorizado aplicando buenas prácticas de desarrollo, principios SOLID y patrones de diseño, manteniendo la funcionalidad original del sistema.

---

## Arquitectura del Sistema
El proyecto sigue una arquitectura basada en el patrón MVC (Model–View–Controller) adaptado al ecosistema de Django, donde:
- Los Models representan la estructura de datos y la lógica de persistencia.
- Las Views actúan como controladores del flujo de la aplicación.
- Los Templates manejan la presentación.
- Se incorporaron capas adicionales como Services y Repositories para mejorar la organización del código.

---

## Buenas Prácticas Aplicadas
Se aplicó una correcta separación de responsabilidades, evitando que las vistas contengan lógica de negocio compleja. La lógica fue trasladada a servicios especializados y el acceso a datos se centralizó en repositorios, logrando un código más limpio, modular y mantenible.

---

## Principios SOLID Implementados

### Open/Closed Principle (OCP)
El sistema fue diseñado para permitir la extensión de funcionalidades sin modificar el código existente. Un ejemplo claro es el manejo de métodos de pago en el checkout, donde es posible agregar nuevos métodos creando nuevas clases sin alterar las ya implementadas.

### Dependency Inversion Principle (DIP)
Las vistas no dependen directamente de implementaciones concretas, sino de servicios abstraídos que encapsulan la lógica de negocio. Esto reduce el acoplamiento entre componentes y facilita futuras modificaciones o ampliaciones del sistema.

---

## Patrones de Diseño Utilizados

### Service Layer
Se implementó una capa de servicios para manejar la lógica de negocio del sistema, como el procesamiento del checkout y la validación de órdenes. Esto permite reutilizar lógica, mejorar la legibilidad del código y mantener las vistas simples.

### Strategy Pattern
Se utilizó el patrón Strategy para gestionar diferentes métodos de pago dentro del checkout. Cada método de pago se implementa como una estrategia independiente, permitiendo cambiar o agregar nuevas formas de pago sin afectar el flujo principal del sistema.
