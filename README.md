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

## Preparación de la información
  * Paso 0. Crear una carpeta en `/audios_para_procesar` con el nombre de la voz a entrenar y colocar los archivos wav dentro.
  * Paso 1. Ejecutar `python process.py`. Se crearán los archivos dentro de su correspondiente subcarpeta en `/voces_procesadas/`, y el txt para la posterior transcripción. Este procedimiento convierte los audios a:
    * mono
    * 32 bits flotante
    * 22.050Mhz
    * una duración no mayor a los 10 segundos
  * Paso 3. Realizar transcripción de los textos usando como base el archivo `transcript.txt`:
    * reemplazar los `*` con la transcripción del archivo. En el primero dejar los caracteres en formato númerico (3, 22) y signos. En el segundo `*`, eliminar toda clase de signos (excepto ¿?¡!-.,;:...), y colocar números en formato alfabético (tres, veintidós).
    * respetar las palabras exactas, acentos, interjeciones y onomatopeyas, de otro modo el resultado no será satisfactorio.

## Entrenamiento / Transferencia
  * Paso 0. Para transerencias, descargar el modelo en español de [css10](https://github.com/Kyubyong/css10) o alguno semejante.
  * Paso 1. Colocar las carpetas `logdir-1` y `logdir-2` de ese modelo dentro de la carpeta creada para la nueva voz.
  * Paso 2. Si se lo desea, ajustar parámetros de configuración en `hyperparams.py`.
  * Paso 3. Para procedimientos hechos por primera vez, setear `prepro=True` para generar archivos megs y mels, y ejecutar por única vez `python prepro.py`.
  * Paso 4. Ejecutar `python train.py 1` para entrenar Text2Mel. En transferencias, se recomienda entrenar al menos de 35K a 50K para obtener buenos resultados.
  * Paso 5. Ejecutar `python train.py 2` para entrenar SSRN. En transferencias, se recomienda entrenar al menos 10K.

Pasos 4 y 5 pueden ejecutarse al mismo tiempo si se dipone más de una GPU.

## Creación de muestras
  * Ejecutar `python synthesize.py` y revisar archivos exportados en la carpeta `samples`.
  * Los caracteres válidos para la sitetización son `!',-.:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz¡¿ÁÅÉÍÓÚáæèéëíîñóöúü—`

## @TODO
  * Ejemplos
  * Creación de interfaz web para facilitar las transcripciones
  * Adpatación de proyectos Jupyter

## Notas
Dataset usada como base:
```
CSS10: A Collection of Single Speaker Speech Datasets for 10 Language, Park, Kyubyong and Mulc, Thomas, Interspeech, 2019.
```