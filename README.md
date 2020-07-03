# Implementación en TensorFlow de DC-TTS: otro modelo de texto-a-voz (versión para lenguas hispanas).
Esta es una implementación del repositiorio [dc_tts](https://github.com/Kyubyong/dc_tts) basado en la investigación [Efficiently Trainable Text-to-Speech System Based on Deep Convolutional Networks with Guided Attention](https://arxiv.org/abs/1710.08969). Ir al repositiorio original para ver más información u información de otros idiomas.

Ésta es una adaptación a lenguas hispanas. Además, intenta facilitar y centralizar algunas herramientas para el procesamiento de los archivos de audio, su posterior transcripción, entrenamiento del modelo y sintetización de muestras.

## Requerimientos
  * NumPy >= 1.11.1
  * TensorFlow >= 1.3 (Note that the API of `tf.contrib.layers.layer_norm` has changed since 1.3)
  * librosa
  * tqdm
  * matplotlib
  * scipy

## Procedimiento
Se puede entrenar un modelo desde cero siempre y cuando se tenga gran cantidad de material de audio (más de 5 horas, perfectamente transcripto y sincronizado). En caso de no poseerlo, se pueden utilizar modelos previamente entrenados (que correspondan al mismo idioma) realizando una transferencia desde ellos, por lo que el requerimiento de material disminuye drásticamente a unos 30 minutos (no menos). 

## Datasets
Se recomienda usar material en buena calidad de audio, sin ruido de fondo ni glitches y de consistentes características. Para transferencias, se puede utilizar un modelo español ya entrenado subido en [css10](https://github.com/Kyubyong/css10). Con una duración de 23:49:49, es una única voz masculina narrando tres cuentos obtenidos de LibriVox. A partir de este modelo (ya preentrenado hasta 400K), se han obtenido resultados aceptables mediante transferencia incluso en acentos no coincidentes con el original (argentino, por ejemplo) y voces femeninas.

## Preparación del dataset propio
Para materiales obtenidos de entrevistas o charlas casuales:
- Evitar todo momento en que hable un interlocutor distinto.
- Evitar fragmentos donde el audio esté contamindo con ruido o música de fondo, pisado por otra persona, roces de ropa, glitchs de ruido, etc.
- Eliminar risas, estornudos, tos, etc.
- Tratar de mantener todo el dataset en una misma línea de entonación: evitar cambios bruscos en el tono, actuaciones/peronificaciones, falseamiento de acentos, gritos, entonaciones en otro idioma, etc.
- Al editar, evitar pegar frases de entonación muy diferente: separar minimamente (0.2 s) para que puedan ser interpratadas como frases distintas. No hay problema si quedan unidos fragmentos donde el discurso no sea coherente, siempre y cuando la entonación sea continua.
- En frases muy largas e ininterrumpidas donde no haya ningún tipo de pausa o descanso (de unos 10 segundos), tratar de cortar y separar en bloques mediante edición.
- Agregar fades al comienzo y final de cada clip recortado (de unos 100/200ms) para evitar los cortes bruscos. Por otro lado, evitar fades demasiado largos que solapen la voz.
- Evitar palabras cortadas, o en todo caso, si fue pronunciada de ese modo, transcribir la palabra de modo "cortado" también.
- Evitar incluir respiraciones fuertes (sobre todo aspiraciones), muy presentes cuando se usa un micrófono corbatero.
- Eliminar gestos/ruidos vocalizados que no se puedan traducir con palabras claras.
- Normalizar el audio, por clips, a unos -5db.
- Exportar editado en wav

## Procesamiento del dataset
  * Paso 0. Usar [wav_to_transcript](https://github.com/GastonZalba/wav_to_transcript) para preparar los archivos de audio.
  * Paso 1. Mover los archivos de audio generados y el transcript final a una subcarpeta dentro de voces_procesadas.


## Entrenamiento / Transferencia
  * Paso 0. Para tranferencias, descargar el modelo en español de [css10](https://github.com/Kyubyong/css10) o alguno semejante.
  * Paso 1. Colocar las carpetas `logdir-1` y `logdir-2` de ese modelo dentro de la carpeta creada para la nueva voz.
  * Paso 2. Si se lo desea, ajustar parámetros de configuración en `hyperparams.py`.
  * Paso 3. Para procedimientos hechos por primera vez, setear `prepro=True` para generar archivos megs y mels, y ejecutar por única vez `python prepro.py`.
  * Paso 4. Ejecutar `python train.py 1` para entrenar Text2Mel. En transferencias, se recomienda entrenar al menos de 35K a 50K para obtener buenos resultados.
  * Paso 5. Ejecutar `python train.py 2` para entrenar SSRN. En transferencias, se recomienda entrenar al menos 10K.

Pasos 4 y 5 pueden ejecutarse al mismo tiempo si se dipone más de una GPU.

## Creación de muestras
  * Ejecutar `python synthesize.py` y revisar archivos exportados en la carpeta `samples`.
  * Los caracteres válidos para la sitetización son `!',-.:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz¡¿ÁÅÉÍÓÚáæèéëíîñóöúü—`

## Ejemplos
[Jorge Luis Borges](https://soundcloud.com/gaston-zalba-261494881/sets/dc_tts_borges_451k) - 451K
<img src="https://i1.sndcdn.com/artworks-YcIk2uBRdHp0TLzR-1ow4SA-t200x200.jpg" height="100" align="right"/>
<br>

## @TODO
  * Creación de interfaz web para facilitar las transcripciones
  * Adpatación de proyectos Jupyter

## Notas
Dataset usada como base:
```
CSS10: A Collection of Single Speaker Speech Datasets for 10 Language, Park, Kyubyong and Mulc, Thomas, Interspeech, 2019.
```