# Sistema de Búsqueda de respuestas adaptable a distintos dominios

Trabajo de fin de grado de Ingeniería informática del curso académico 2017/2018.

## Integrantes
-Gabriel Sellés Salvà <gabriese@ucm.es>

-Aitor Cayón Ruano    <aitorcay@ucm.es>

-Fernando Pérez Gutiérrez  <fernaper@ucm.es>

-Jose Javier Cortés Tejada  <josejaco@ucm.es>


## Directores
- Antonio F. G. Sevilla <afgs@ucm.es>

- Alberto Díaz <albertodiaz@fdi.ucm.es>

## Resumen 

En la actualidad, los sistemas de búsqueda de respuestas tienen un papel destacable tanto en la sociedad como en la industria. Debido a su utilidad, a lo largo de la historia reciente, se han realizado distintos tipos de implementaciones, cada una centrándose en su finalidad concreta. Aún así, la mayoría de implementaciones basan su funcionamiento en estudios estadísticos y modelos entrenados con gran volumen de datos.

En este proyecto hemos optado por implementar un sistema con un enfoque distinto: un sistema de búsqueda de respuestas que resuelva consultas mediante el análisis lingüístico de conocimiento textual. 

Además, el sistema  implementado, es adaptable a múltiples dominios. Esto implica que tiene la capacidad de utilizar distintas fuentes de información textual a la hora de responder a una consulta introducida por el usuario. Esta funcionalidad permite la resolución de consultas de distintos ámbitos y dominios, a la vez que facilita considerablemente la inserción de nuevas fuentes de información textual.

Para realizar esta implementación, este proyecto consta de varias partes diferenciadas: 
 	-Análisis de la consulta introducida: se realiza un análisis sintáctico y semántico de la consulta introducida por el usuario. 
  
 	-Obtención información textual: se buscan documentos que contengan las palabras clave de la consulta introducida y, por lo tanto, potencialmente contengan la respuesta a la consulta.
  
 	-Obtención de la respuesta: se busca en dichos documentos el fragmento que responde a la consulta.
  
 	-Generación de la respuesta final: se genera una sentencia en lenguaje natural que contiene la respuesta.
 
Por último, se ha ejecutado el sistema sobre un repositorio propio, BioASQ y Simple Wikipedia para evaluar las capacidades de este.

## Abstract  
At present, question answering systems have great relevance both in society and industry. Due to its utility, in recent history, they have been implemented in several ways, each of them with a specific purpose. Nevertheless, most of implementations are based on statistical studies or models trained with a large amount of data.

We have decided to implement our system with a different approach: a question answering system capable of solving queries through linguistic analysis using textual knowledge.

In addition, the implemented system can be adapted to multiple domains. This implies we can use different sources of textual information when answering the query introduced by the user. This functionality allows the resolution of queries from different fields and domains while considerably simplifying the insertion of new sources of textual information.

The implementation of this project has been divided in different parts:

 -Analysis of the introduced query: executes the syntactic and semantic analysis of the query introduced by the user.
 
 -Textual information retrieval:  searches for the documents containing keywords from the introduced query and posibly containing the answer to it.
 
 -Answer retrieval: } searches for the fragment in the documents answering the query.
 
 -Generation of the final answer:  generates a natural language sentence containing the answer.
 
Finally, the system has been executed over our own repository, BioASQ and Simple Wikipedia in order to validate its capabilites.
