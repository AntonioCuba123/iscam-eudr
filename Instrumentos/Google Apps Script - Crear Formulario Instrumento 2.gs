/**
 * Crea el Google Form completo de Instrumento 2 (Encuesta Cuantitativa EUDR) — 75 preguntas,
 * y lo enlaza a un Google Sheet nuevo donde caerán las respuestas.
 *
 * CÓMO USARLO:
 * 1. Ir a https://script.google.com -> Proyecto nuevo.
 * 2. Pegar este archivo completo, reemplazando el contenido de Code.gs.
 * 3. Ejecutar la función crearInstrumento2() (menú Ejecutar, o botón ▶).
 * 4. La primera vez pedirá autorización — aceptar (es tu propia cuenta de Google).
 * 5. Al terminar, revisar el "Registro de ejecución" (Ver > Registros) — ahí quedan
 *    la URL de edición del formulario y la URL de la hoja de cálculo de respuestas.
 *
 * Fuente: Instrumento 2 - Encuesta Cuantitativa.md (2026-09-17, 75 preguntas,
 * incluye las adiciones del Manual PROMPERÚ/BID en D3/D5 y P11/P12 de validación externa ISCAM).
 */
function crearInstrumento2() {
  var form = FormApp.create('Instrumento 2 — Encuesta Cuantitativa EUDR');
  form.setDescription(
    'Diagnóstico de preparación frente al Reglamento (UE) 2023/1115 (EUDR). ' +
    'Escala 0-4 en preguntas de madurez: 0=No existe/No sabe · 1=Informal o parcial · ' +
    '2=En desarrollo · 3=Implementado · 4=Implementado y verificado/auditado. ' +
    'No es una auditoría — responder "No" o "No verificado" es información válida, no un mal resultado.'
  );
  form.setCollectEmail(false);
  form.setProgressBar(true);


  form.addSectionHeaderItem().setTitle('Bloque 0 — Ficha de identificación');

  form.addTextItem().setTitle('0.1. Nombre de la cooperativa / razón social').setRequired(true);
  form.addTextItem().setTitle('0.2. RUC').setRequired(true);
  form.addCheckboxItem().setTitle('0.3. Producto(s) exportado(s)').setChoiceValues(['Café', 'Cacao', 'Madera', 'Otro']).setRequired(true);
  form.addTextItem().setTitle('0.3b. Código SA (si se conoce)').setRequired(false);
  form.addTextItem().setTitle('0.4a. N.º de socios productores').setRequired(true);
  form.addTextItem().setTitle('0.4b. Hectáreas totales asociadas').setRequired(true);
  form.addMultipleChoiceItem().setTitle('0.5. ¿Exporta directamente a la UE o a través de un tercero?').setChoiceValues(['Directamente', 'A través de un tercero']).setRequired(true);
  form.addTextItem().setTitle('0.6. Si es indirecto: ¿quién es el comprador que sí exporta a la UE?').setRequired(false);
  form.addTextItem().setTitle('0.7. Volumen anual aproximado destinado a la UE (% del total)').setRequired(true);
  form.addTextItem().setTitle('0.8. País(es) de destino dentro de la UE').setRequired(true);
  form.addCheckboxItem().setTitle('0.9. Certificaciones voluntarias vigentes').setChoiceValues(['Rainforest Alliance', 'Fairtrade', 'Orgánico', 'UTZ', 'Otra', 'Ninguna']).setRequired(true);
  form.addTextItem().setTitle('0.9b. Si marcó "Otra": especifique').setRequired(false);
  form.addMultipleChoiceItem().setTitle('0.10. Dispersión geográfica de los socios').setChoiceValues(['Un solo distrito', 'Varios distritos, misma provincia', 'Varias provincias o regiones']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('0.11. Distancia aproximada entre las parcelas más alejadas y el centro de acopio').setChoiceValues(['Menos de 5 km', 'Entre 5 y 20 km', 'Entre 20 y 50 km', 'Más de 50 km', 'No se ha medido']).setRequired(true);
  form.addTextItem().setTitle('0.12. % de mujeres en la directiva/consejo directivo').setRequired(true);

  form.addSectionHeaderItem().setTitle('Bloque P — Variables de performance');

  form.addTextItem().setTitle('P1. Volumen exportado a la UE en el último año (kg o toneladas — especifique unidad y producto)').setRequired(true);
  form.addTextItem().setTitle('P1b. Volumen TOTAL exportado a todos los destinos (UE y no UE) en el último año, misma unidad que P1').setRequired(true);
  form.addTextItem().setTitle('P2. Volumen exportado a la UE hace 3 años, mismo producto (retrospectivo — dejar vacío si no está seguro)').setRequired(false);
  form.addTextItem().setTitle('P3. Ingreso total por ventas de exportación a la UE en el último año (S/ o USD)').setRequired(true);
  form.addTextItem().setTitle('P4. N.º de compradores/clientes europeos activos actualmente').setRequired(true);
  form.addTextItem().setTitle('P5. N.º de compradores europeos activos hace 3 años (retrospectivo)').setRequired(false);
  form.addTextItem().setTitle('P6. Precio promedio pagado al socio productor por kg/quintal, último año (S/ o USD)').setRequired(true);
  form.addTextItem().setTitle('P7. Precio promedio pagado al socio productor, hace 3 años (retrospectivo)').setRequired(false);
  form.addMultipleChoiceItem().setTitle('P8. ¿Lote rechazado u observado por un comprador europeo por trazabilidad/deforestación en los últimos 2 años?').setChoiceValues(['Sí', 'No', 'No sabe']).setRequired(true);
  form.addTextItem().setTitle('P9. Si la anterior es "Sí": N.º aproximado de lotes rechazados u observados').setRequired(false);
  form.addMultipleChoiceItem().setTitle('P10. ¿Ha perdido algún contrato o comprador europeo en los últimos 2 años por motivos de cumplimiento?').setChoiceValues(['Sí', 'No', 'No sabe']).setRequired(true);
  form.addTextItem().setTitle('P11. % del volumen total exportado con trazabilidad completa verificada hasta la parcela de origen').setRequired(true);
  form.addTextItem().setTitle('P12. N.º de años consecutivos exportando a la Unión Europea (contando el año actual)').setRequired(true);

  form.addSectionHeaderItem().setTitle('D1 — Clasificación regulatoria');

  form.addMultipleChoiceItem().setTitle('1. ¿La cooperativa introduce el producto directamente en el mercado de la UE bajo su propio nombre?').setChoiceValues(['Sí', 'No']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('2. ¿Transforma el producto (trilla, tostado, fermentado, aserrío) antes de venderlo?').setChoiceValues(['Transforma', 'No transforma']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('3. ¿Sabe con certeza qué rol le corresponde (operador, operador posterior, comerciante, micro/pequeño operador primario)?').setChoiceValues(['Sí con certeza', 'Idea aproximada', 'No sabe']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('4. ¿Cumple los umbrales de microempresa/pequeña empresa (Directiva 2013/34/UE)?').setChoiceValues(['Sí', 'No', 'No sabe']).setRequired(true);

  form.addSectionHeaderItem().setTitle('D2 — Trazabilidad y geolocalización');

  form.addScaleItem().setTitle('5. ¿Existe registro de geolocalización (GPS/polígono) por parcela de socio?').setHelpText('0=No existe/No sabe · 1=Informal o parcial · 2=En desarrollo · 3=Implementado · 4=Implementado y verificado/auditado').setBounds(0, 4).setLabels('No existe / No sabe', 'Implementado y verificado').setRequired(true);
  form.addTextItem().setTitle('6. % de socios con parcela geolocalizada').setRequired(true);
  form.addScaleItem().setTitle('7. ¿El sistema vincula un lote exportado con la(s) parcela(s) específica(s)?').setHelpText('0=No existe/No sabe · 1=Informal o parcial · 2=En desarrollo · 3=Implementado · 4=Implementado y verificado/auditado').setBounds(0, 4).setLabels('No existe / No sabe', 'Implementado y verificado').setRequired(true);
  form.addMultipleChoiceItem().setTitle('8. ¿Quién levantó la información de geolocalización?').setChoiceValues(['Técnico propio', 'Consultor', 'Proyecto de cooperación', 'Socio por su cuenta', 'No se ha levantado']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('9. Frecuencia de actualización del registro').setChoiceValues(['Nunca', 'Al ingreso del socio', 'Anual', 'Por cosecha']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('10. ¿Existe algún punto de acopio/beneficio donde se mezclan lotes de distinto origen sin registro? (bandera)').setChoiceValues(['Sí, se mezclan sin control', 'Se mezclan pero con registro de origen', 'No, se mantiene segregación física completa']).setRequired(true);

  form.addSectionHeaderItem().setTitle('D3 — Legalidad de la producción');

  form.addTextItem().setTitle('11. % de socios con título de propiedad o posesión reconocida legalmente').setRequired(true);
  form.addMultipleChoiceItem().setTitle('12. ¿Hay parcelas superpuestas a áreas protegidas, reservas comunales o territorios indígenas sin sanear?').setChoiceValues(['Sí extensa', 'Sí puntual', 'No verificado', 'No, ninguna']).setRequired(true);
  form.addScaleItem().setTitle('13. ¿Se verifica cumplimiento laboral (no trabajo infantil, seguridad social) a nivel de finca?').setHelpText('0=No existe/No sabe · 1=Informal o parcial · 2=En desarrollo · 3=Implementado · 4=Implementado y verificado/auditado').setBounds(0, 4).setLabels('No existe / No sabe', 'Implementado y verificado').setRequired(true);
  form.addMultipleChoiceItem().setTitle('14. ¿Alguna parcela se ubica en zona de desarrollo alternativo (ex-coca) o con antecedentes de conflicto social/territorial?').setChoiceValues(['Sí', 'No', 'No verificado']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('14a. ¿Los socios cuentan con autorización de uso de agua para su actividad productiva, cuando corresponde?').setChoiceValues(['Sí, todas las fuentes verificadas', 'Parcialmente', 'No', 'No aplica']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('14b. ¿El tratamiento de aguas residuales del beneficio/procesamiento cumple con lo exigido por la autoridad ambiental?').setChoiceValues(['Siempre', 'A veces', 'No', 'No aplica']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('14c. ¿Alguna parcela se encuentra dentro de la faja marginal de un río, quebrada, lago o laguna?').setChoiceValues(['Sí', 'No', 'No sabe']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('14e. ¿La cooperativa y sus socios están al día en sus obligaciones tributarias, aduaneras y comerciales?').setChoiceValues(['Sí, verificado', 'Parcialmente', 'No verificado', 'No sabe']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('14f. ¿Existen políticas o mecanismos internos contra la corrupción (código de conducta, canal de denuncias)?').setChoiceValues(['Sí, formalizado', 'Informal', 'No existe']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('14g. Cuando corresponde, ¿se ha realizado un proceso de Consentimiento Libre, Previo e Informado (CLPI)?').setChoiceValues(['Sí, proceso documentado', 'Aplica pero no se ha realizado', 'No aplica, no hay territorios de este tipo', 'No sabe']).setRequired(true);

  form.addSectionHeaderItem().setTitle('D4 — Riesgo de deforestación');

  form.addMultipleChoiceItem().setTitle('15. ¿Se verificó cambio de uso de suelo posterior al 31 dic. 2020?').setChoiceValues(['No verificado', 'Verificación parcial', 'Verificado sin hallazgos', 'Casos detectados sin resolver', 'Verificado sistemáticamente y documentado']).setRequired(true);
  form.addScaleItem().setTitle('16. ¿Usa herramientas de monitoreo satelital (Global Forest Watch, plataformas nacionales)?').setHelpText('0=No existe/No sabe · 1=Informal o parcial · 2=En desarrollo · 3=Implementado · 4=Implementado y verificado/auditado').setBounds(0, 4).setLabels('No existe / No sabe', 'Implementado y verificado').setRequired(true);
  form.addMultipleChoiceItem().setTitle('17. ¿Conoce la clasificación de riesgo (bajo/estándar/alto) de su zona?').setChoiceValues(['Sí documentado', 'Idea aproximada', 'No sabe']).setRequired(true);

  form.addSectionHeaderItem().setTitle('D5 — Sistema interno de diligencia debida');

  form.addScaleItem().setTitle('18. ¿Existe procedimiento escrito de diligencia debida?').setHelpText('0=No existe/No sabe · 1=Informal o parcial · 2=En desarrollo · 3=Implementado · 4=Implementado y verificado/auditado').setBounds(0, 4).setLabels('No existe / No sabe', 'Implementado y verificado').setRequired(true);
  form.addScaleItem().setTitle('18a. ¿Existe una política de deforestación formal y escrita, con objetivos, metas medibles y plazos?').setHelpText('0=No existe/No sabe · 1=Informal o parcial · 2=En desarrollo · 3=Implementado · 4=Implementado y verificado/auditado').setBounds(0, 4).setLabels('No existe / No sabe', 'Implementado y verificado').setRequired(true);
  form.addMultipleChoiceItem().setTitle('18b. ¿Prioriza sus riesgos de deforestación con algún criterio de probabilidad e impacto?').setChoiceValues(['No se prioriza, se atiende lo que surge', 'Priorización informal, sin criterio escrito', 'Priorización estructurada con matriz probabilidad×impacto']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('19. ¿Ha elaborado o participado en una declaración de diligencia debida / simplificada?').setChoiceValues(['No sabe qué es', 'No pero lo entiende', 'En proceso', 'Presentada y aceptada']).setRequired(true);
  form.addCheckboxItem().setTitle('19a. Del plan de gestión de riesgos (si existe), ¿qué componentes incluye?').setChoiceValues(['Plazos definidos', 'Recursos (humanos/financieros) asignados', 'Responsables designados', 'Procedimientos de consulta con socios/comunidades', 'Sistema de seguimiento y monitoreo', 'Protocolo ante incumplimiento de un socio', 'Atención diferenciada a productoras mujeres']).setRequired(false);
  form.addMultipleChoiceItem().setTitle('20. ¿Existe responsable designado para el cumplimiento EUDR?').setChoiceValues(['No', 'Función adicional', 'Dedicado']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('21. ¿Capacitación formal en los últimos 12 meses?').setChoiceValues(['No', 'Hace más de 12 meses', 'Sí, reciente']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('21a. ¿El plan de gestión de riesgos se revisa con una frecuencia definida?').setChoiceValues(['No hay revisión definida', 'Revisión reactiva, sin frecuencia fija', 'Revisión periódica definida']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('21b. ¿La cooperativa elabora y comunica un reporte de diligencia debida con indicadores?').setChoiceValues(['No', 'Sí, uso interno solamente', 'Sí, interno y compartido con compradores u otras partes interesadas']).setRequired(true);

  form.addSectionHeaderItem().setTitle('D6 — Capacidad organizacional y digital');

  form.addMultipleChoiceItem().setTitle('22. Presupuesto asignado para cumplimiento EUDR').setChoiceValues(['No', 'Parcial', 'Sí']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('23. Digitalización de registros').setChoiceValues(['Papel', 'Mixto', 'Digital']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('24. Conectividad a internet').setChoiceValues(['No hay', 'Limitada', 'Confiable']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('25. ¿Ha gestionado apoyo externo para adecuarse?').setChoiceValues(['No y lo necesita', 'No lo cree necesario', 'Sí en el pasado', 'Sí activo']).setRequired(true);

  form.addSectionHeaderItem().setTitle('D7 — Cadena de valor');

  form.addMultipleChoiceItem().setTitle('26. ¿El comprador ha exigido formalmente geolocalización/diligencia debida?').setChoiceValues(['Aún no', 'Informalmente', 'Formalmente por escrito']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('27. ¿El comprador ofrece financiamiento/asistencia técnica condicionada al cumplimiento?').setChoiceValues(['Sí', 'No']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('28. Riesgo percibido de perder el contrato si no cumple a tiempo').setChoiceValues(['No sabe', 'Bajo', 'Medio', 'Alto']).setRequired(true);

  form.addSectionHeaderItem().setTitle('D8 — Gobernanza interna y apropiación de los socios');

  form.addScaleItem().setTitle('29. ¿Se han realizado asambleas o reuniones informativas sobre el EUDR dirigidas a los socios?').setHelpText('0=No existe/No sabe · 1=Informal o parcial · 2=En desarrollo · 3=Implementado · 4=Implementado y verificado/auditado').setBounds(0, 4).setLabels('No existe / No sabe', 'Implementado y verificado').setRequired(true);
  form.addTextItem().setTitle('30. % estimado de socios que entienden por qué se les pide geolocalización/documentación').setRequired(true);
  form.addMultipleChoiceItem().setTitle('31. ¿Existe algún mecanismo interno para que los socios entreguen su información de parcela?').setChoiceValues(['No existe', 'Se pide informalmente', 'Es requisito formal para vender a la cooperativa']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('32. Rotación de la directiva en los últimos 2 años').setChoiceValues(['Alta', 'Moderada', 'Baja/estable']).setRequired(true);

  form.addSectionHeaderItem().setTitle('D9 — Sostenibilidad económica del cumplimiento');

  form.addMultipleChoiceItem().setTitle('33. Estimación del costo total de adecuación frente al presupuesto anual').setChoiceValues(['Costo mayor al 10% del presupuesto anual', 'Entre 3–10%', 'Menor al 3%', 'No se ha estimado']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('34. ¿La cooperativa ha financiado la adecuación con deuda?').setChoiceValues(['Sí', 'No', 'No ha sido necesario']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('35. ¿Existe riesgo de que el costo de adecuación se traslade a un menor precio pagado al socio?').setChoiceValues(['Sí, ya ha ocurrido', 'Es un riesgo latente', 'No aplica', 'No se ha evaluado']).setRequired(true);

  form.addSectionHeaderItem().setTitle('D10 — Confusión entre certificación voluntaria y cumplimiento EUDR');

  form.addMultipleChoiceItem().setTitle('36. ¿La cooperativa cree que su certificación vigente ya cubre las obligaciones del EUDR?').setChoiceValues(['Sí, totalmente', 'Sí, en parte', 'No, sabe que son cosas distintas', 'No tiene certificación']).setRequired(true);
  form.addMultipleChoiceItem().setTitle('37. ¿Algún proveedor o consultor le ha ofrecido una "certificación EUDR" como producto?').setChoiceValues(['Sí', 'No']).setRequired(true);

  form.addSectionHeaderItem().setTitle('D11 — Ecosistema de apoyo externo');

  form.addCheckboxItem().setTitle('38. Actores con los que la cooperativa ya tiene contacto o apoyo activo').setChoiceValues(['SERFOR (legalidad forestal)', 'PNCB-MINAM (monitoreo satelital)', 'MIDAGRI o programa regional de café-cacao', 'Gobierno regional (catastro/saneamiento)', 'Cooperación internacional (GIZ, USAID, UE, ONG)', 'Junta Nacional del Café, APPCACAO u otro gremio', 'Ninguno']).setRequired(true);
  form.addParagraphTextItem().setTitle('39. De los actores no marcados arriba, ¿cuáles conoce pero no ha contactado, y por qué?').setRequired(false);

  // Crear la hoja de cálculo de respuestas y enlazarla al formulario
  var ss = SpreadsheetApp.create('Instrumento 2 — Respuestas (piloto EUDR)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log('Formulario creado.');
  Logger.log('URL de edición (para revisar/ajustar antes de compartir): ' + form.getEditUrl());
  Logger.log('URL pública (para compartir con las cooperativas): ' + form.getPublishedUrl());
  Logger.log('Google Sheet de respuestas: ' + ss.getUrl());
}
