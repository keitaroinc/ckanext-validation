��    v      �              |  6   }  �   �  �   c     	     	  A  )	  ]  k
  Z  �  &  $     K  	   X     b  M   h     �     �     �  j   �  d   T  �   �  �   S  �   
  �   �     �     �     �     �     �  )   �          #     1     I     V     b  
   o  T   z  )   �  V   �     P     Y     a     n     s     x     �     �     �     �     �  -   �          1     2  �   E     �       >   (  =   g  $   �  6   �  L        N     [     m     z     �  #   �  .   �  J   �  `   ;  I   �  I   �  J   0  9   {  	  �    �      �  ^  �  x   U  {   �  �   J  {   �  �   I   {   �   s   H!  
   �!  3   �!  2   �!  .  ."  r  ]#  O  �$  =   &  :  ^'  1  �(  b  �)  \  .+  �   �,  @  C-     �.  4   �.  +   �.     �.     /  ,   /     @/  
   U/     `/     r/     �/     �/     �/     �/     �/     �/  	   �/     �/     �/  }  �/  ?   Q1  �   �1  �   Q2     3     +3  p  93  �  �4  �  K6  B  �7     39     J9     a9  ]   h9     �9  !   �9  $   �9  �   ":  �   �:  �   ?;  �   <  �   =  ;  �=  ,   #?     P?     b?     s?     �?  5   �?     �?     �?     �?     @     @     ,@     <@  _   J@  :   �@  d   �@     JA     SA     aA     zA     A     �A  !   �A     �A  !   �A     �A     B  3   B     CB  6  ZB     �C  �   �C     �D     �D  K   �D  H   E  7   ME  A   �E  V   �E     F     .F     LF     [F     nF  -   �F  >   �F  L   �F  x   EG  d   �G  d   #H  W   �H  G   �H  G  (I  4  pJ  '   �K  �  �K  u   rM  w   �M  �   `N  v   �N  �   ^O  w   �O  z   \P     �P  6   �P  9   Q  Y  LQ  �  �R  �  LT  v  �U  r  MW  o  �X  �  0Z  �  �[  �   �]  j  v^     �_  K   �_  5   E`     {`     �`  A   �`  "   �`     �`     a     !a     :a  
   Ta     _a     ea     na     |a  
   �a     �a  
   �a   
Please report this to https://github.com/chjj/marked. 
There are validation issues with this file, please see the
<a {params}>report</a> for details. Once you have resolved the issues,
click the button below to replace the file.  You can pass a JSON object of validation options. See <a href="https://github.com/frictionlessdata/ckanext-validation#validation-options">here</a> for more information.  valid table(s)  warning(s) A column in the header row is missing a value. Column names should be provided.

 How it could be resolved:
 - Add the missing column name to the first row of the data source.
 - If the first row starts with, or ends with a comma, remove it.
 - If this error should be ignored disable `blank-header` check in {validator}. A lenght of this field value should be greater or equal than schema constraint value.

 How it could be resolved:
 - If this value is not correct, update the value.
 - If value is correct, then remove or refine the `minimumLength` constraint in the schema.
 - If this error should be ignored disable `minimum-length-constraint` check in {validator}. A lenght of this field value should be less or equal than schema constraint value.

 How it could be resolved:
 - If this value is not correct, update the value.
 - If value is correct, then remove or refine the `maximumLength` constraint in the schema.
 - If this error should be ignored disable `maximum-length-constraint` check in {validator}. Based on the schema there should be a header that is missing in the first row of the data source.

 How it could be resolved:
 - Add the missing column to the data source or remove the extra field from the schema
 - If this error should be ignored disable `missing-header` check in {validator}. Blank Header Blank Row Clear Column {column_number} is a required field, but row {row_number} has no value Data Schema Data Schema URL Data Validation Report Data reading error because of HTTP error.

 How it could be resolved:
 - Fix url link if it's not correct. Data reading error because of IO error.

 How it could be resolved:
 - Fix path if it's not correct. Data reading error because of an encoding problem.

 How it could be resolved:
 - Fix data source if it's broken.
 - Set correct encoding in {validator}. Data reading error because of incorrect format.

 How it could be resolved:
 - Fix data format (e.g. change file extension from `txt` to `csv`).
 - Set correct format in {validator}. Data reading error because of incorrect scheme.

 How it could be resolved:
 - Fix data scheme (e.g. change scheme from `ftp` to `http`).
 - Set correct scheme in {validator}. Data reading error because of not supported or inconsistent contents.

 How it could be resolved:
 - Fix data contents (e.g. change JSON data to array or arrays/objects).
 - Set correct source settings in {validator}. Data validation unknown Duplicate Header Duplicate Row Duration Encoding Error Enter manually a Table Schema JSON object Enumerable Constraint Error details Error during validation Extra Header Extra Value Format Error HTTP Error Header in column {column_number} doesn't match field name {field_name} in the schema Header in column {column_number} is blank Header in column {column_number} is duplicated to header in column(s) {column_numbers} IO Error Invalid Invalid data JSON Link Maximum Constraint Maximum Length Constraint Minimum Constraint Minimum Length Constraint Missing Header Missing Value No validation report exists for this resource Non-Matching Header One of the data source headers doesn't match the field name defined in the schema.

 How it could be resolved:
 - Rename header in the data source or field in the schema
 - If this error should be ignored disable `non-matching-header` check in {validator}. Pattern Constraint Provided schema is not valid.

 How it could be resolved:
 - Update schema descriptor to be a valid descriptor
 - If this error should be ignored disable schema cheks in {validator}. Required Constraint Resource was not found. Row {row_number} has a missing value in column {column_number} Row {row_number} has an extra value in column {column_number} Row {row_number} is completely blank Row {row_number} is duplicated to row(s) {row_numbers} Rows {row_numbers} has unique constraint violation in column {column_number} Scheme Error Show next 10 rows Source Error Success details Table Schema Error Table Schema error: {error_message} Table inspection has reached 1000 row(s) limit The data source could not be successfully decoded with {encoding} encoding The data source has not supported or has inconsistent contents; no tabular data can be extracted The data source is in an unknown format; no tabular data can be extracted The data source is in an unknown scheme; no tabular data can be extracted The data source returned an HTTP error with a status code of {status_code} The data source returned an IO Error of type {error_type} The exact same data has been seen in another row.

 How it could be resolved:
 - If some of the data is incorrect, correct it.
 - If the whole row is an incorrect duplicate, remove it.
 - If this error should be ignored disable `duplicate-row` check in {validator}. The first row of the data source contains header that doesn't exist in the schema.

 How it could be resolved:
 - Remove the extra column from the data source or add the missing field to the schema
 - If this error should be ignored disable `extra-header` check in {validator}. The full list of error messages: The value does not match the schema type and format for this field.

 How it could be resolved:
 - If this value is not correct, update the value.
 - If this value is correct, adjust the type and/or format.
 - To ignore the error, disable the `type-or-format-error` check in {validator}. In this case all schema checks for row values will be ignored. The value {value} in row {row_number} and column {column_number} does not conform to the given enumeration: {constraint} The value {value} in row {row_number} and column {column_number} does not conform to the maximum constraint of {constraint} The value {value} in row {row_number} and column {column_number} does not conform to the maximum length constraint of {constraint} The value {value} in row {row_number} and column {column_number} does not conform to the minimum constraint of {constraint} The value {value} in row {row_number} and column {column_number} does not conform to the minimum length constraint of {constraint} The value {value} in row {row_number} and column {column_number} does not conform to the pattern constraint of {constraint} The value {value} in row {row_number} and column {column_number} is not type {field_type} and format {field_format} There are  There is a missing header in column {column_number} There is an extra header in column {column_number} This field is a required field, but it contains no value.

 How it could be resolved:
 - If this value is not correct, update the value.
 - If value is correct, then remove the `required` constraint from the schema.
 - If this error should be ignored disable `required-constraint` check in {validator}. This field is a unique field but it contains a value that has been used in another row.

 How it could be resolved:
 - If this value is not correct, update the value.
 - If value is correct, then the values in this column are not unique. Remove the `unique` constraint from the schema.
 - If this error should be ignored disable `unique-constraint` check in {validator}. This field value should be equal to one of the values in the enumeration constraint.

 How it could be resolved:
 - If this value is not correct, update the value.
 - If value is correct, then remove or refine the `enum` constraint in the schema.
 - If this error should be ignored disable `enumerable-constraint` check in {validator}. This field value should be greater or equal than constraint value.

 How it could be resolved:
 - If this value is not correct, update the value.
 - If value is correct, then remove or refine the `minimum` constraint in the schema.
 - If this error should be ignored disable `minimum-constraint` check in {validator}. This field value should be less or equal than constraint value.

 How it could be resolved:
 - If this value is not correct, update the value.
 - If value is correct, then remove or refine the `maximum` constraint in the schema.
 - If this error should be ignored disable `maximum-constraint` check in {validator}. This field value should conform to constraint pattern.

 How it could be resolved:
 - If this value is not correct, update the value.
 - If value is correct, then remove or refine the `pattern` constraint in the schema.
 - If this error should be ignored disable `pattern-constraint` check in {validator}. This row has less values compared to the header row (the first row in the data source). A key concept is that all the rows in tabular data must have the same number of columns.

 How it could be resolved:
 - Check data is not missing a comma between the values in this row.
 - If this error should be ignored disable `missing-value` check in {validator}. This row has more values compared to the header row (the first row in the data source). A key concept is that all the rows in tabular data must have the same number of columns.

 How it could be resolved:
 - Check data has an extra comma between the values in this row.
 - If this error should be ignored disable `extra-value` check in {validator}. This row is empty. A row should contain at least one value.

 How it could be resolved:
 - Delete the row.
 - If this error should be ignored disable `blank-row` check in {validator}. Two columns in the header row have the same value. Column names should be unique.

 How it could be resolved:
 - Add the missing column name to the first row of the data.
 - If the first row starts with, or ends with a comma, remove it.
 - If this error should be ignored disable `duplicate-header` check in {validator}. Type or Format Error URL for a Data Schema file available on the Internet Unauthorized to read this validation report Unique Constraint Upload Upload a Data Schema file from your computer Uploaded Data Schema Valid data Validation Report Validation timestamp Warning details data error failure invalid schema structure success unknown Project-Id-Version: ckanext-validation 0.0.4
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2018-08-13 11:22+0200
PO-Revision-Date: 2018-08-10 12:20+0200
Last-Translator: 
Language: sq
Language-Team: sq <LL@li.org>
Plural-Forms: nplurals=2; plural=(n != 1)
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.3.4
 
Ju lutemi raportoni këtë tek https://github.com/chjj/marked. 
Ka probleme të validimit me këtë skedar, ju lutem shikoni
<a {params}>rarort</a> për detajet. Pasi ta keni zgjidhur problemin,
klikoni butonin më poshtë për ta zëvendësuar skedarin. Ju mund të kaloni një objekt JSON të opsioneve të validimit. Shikoni <a href="https://github.com/frictionlessdata/ckanext-validation#validation -options"> këtu </a> për më shumë informacion.  tabela e vlefshme paralajmërim Në një kolonë në fillimin e rreshtit mungon vlera. Emri i kolonës duhet të sigurohet
  Si mund të zgjidhet:
  - Shto emrin e kolonës që mungon në rreshtin e parë të burimit të të dhënave.
  - Nëse fillon rreshti i parë ose përfundon me presje, hiqeni atë.
  - Nëse ky gabim duhet të injorohet, çaktivizoni `blank-header` check in {validator}. Gjatësia e kësaj vlere në terren duhet të jetë më e madhe ose e barabartë sesa vlera e kufizimit të skemës.

  Si mund të zgjidhet:
  - Nëse kjo vlerë nuk është e saktë, përditësoni vlerën.
  - Nëse vlera është e saktë, atëherë hiqni ose përsosni kufizimin `minimumLength` në skemë.
  - Nëse ky gabim duhet të injorohet, çaktivizoni 'minimum-length-constraint` check in {validator}. Një gjatësi e kësaj vlere në terren duhet të jetë më e ulët ose e barabartë sesa vlera e kufizimit të skemës.

  Si mund të zgjidhet:
  - Nëse kjo vlerë nuk është e saktë, përditësoni vlerën.
  - Nëse vlera është e saktë, atëherë hiqni ose përsosni kufizimin `maximumLength` në skemë.
  - Nëse ky gabim duhet të injorohet, çaktivizoni `maximum-length-constraint` check in {validator}. Bazuar në skemën duhet të ketë një titull i cili mungon në rreshtin e parë të burimit të të dhënave.

  Si mund të zgjidhet:
  - Shto kolonën e humbur në burimin e të dhënave ose hiqeni fushën shtesë nga skema
  - Nëse ky gabim duhet të injorohet, çaktivizoni 'missing-header` check in {validator}. Titulli i paplotësuar Rreshti i paplotësuar Qartë Kolona {column_number} është një fushë e kërkuar, por rreshti {row_number} nuk ka vlerë Skema e të Dhënave URL-ja e skemës së të dhënave Raporti i Validimit të të Dhënave Gabim gjatë leximit të të dhënave për shkak të gabimit HTTP.
Si mund të zgjidhet:
  - Rregullo url link-un nëse nuk është e saktë. Gabim gjatë leximit të të dhënave për shkak të gabimit të IO.

  Si mund të zgjidhet:
- Rregullo rrugën nëse nuk është e saktë. Gabim gjatë leximit të të dhënave për shkak të një problemi me kodimin.

  Si mund të zgjidhet:
  - Përcaktoni burimin e të dhënave nëse është i prishur.
  - Vendosja e kodimit të saktë në {validator}. Gabim gjatë leximit të të dhënave për shkak të formatit të gabuar.
 Si mund të zgjidhet:
- Përcaktoni përmbajtjen e skemës (p.sh. skema e ndryshimit nga `ftp` në` http`).
- Vendosni formatin e saktë në {validator}. Gabim gjatë leximit të të dhënave për shkak të skemës së gabuar.
 Si mund të zgjidhet:
- Përcaktoni përmbajtjen e skemës (p.sh. skema e ndryshimit nga `ftp` në` http`).
- Vendosni skemën e saktë në {validator}. Gabim gjatë leximit të të dhënave për shkak të mungesës së mbështetjes ose të përmbajtjes jokonsistente.

 Si mund të zgjidhet:
 - Përcaktoni përmbajtjen e të dhënave (p.sh. ndryshoni të dhënat e JSON-it tek grupi ose grupet / objektet).
- Vendosni cilësimet e sakta të burimit në {validator}. Validimi i i të dhënave është i panjohur Titulli i dubluar Rresht i dubluar Kohëzgjatja Gabim gjatë kodimit Fusni manualisht një skemë të Tabelës JSON objekt Kufizim i shumëllojshëm Detajet e gabimit Gabim gjatë validimit Titulli shtesë Vlera shtesë Format i gabuar HTTP e gabuar Titulli në kolonën {column_number} nuk përputhet me emrin e fushës {field_name} në skemën Titulli në kolonë {column_number} është i paplotësuar Udhëheqësi në kolonën {column_number} është i dubluar në fillimin e kolonës {column_numbers} IO Gabim I pavlefshëm Të dhënat e pavlefshme JSON Link (Lidhje) Kufizimi minimal Kufizimi maksimal i kohëzgjatjes Kufizimi minimal Kufizimi maksimal i kohëzgjatjes Mungon titulli Mungon vlera Nuk ekziston një raport validimi për këtë burim Titulli nuk përputhet Njëri nga titujt e burimit të të dhënave nuk përputhet me emrin e fushës së përcaktuar në skemë.

  Si mund të zgjidhet:
  - Riemërtoni titullin në burimin e të dhënave ose fushën e skemës
  - Nëse ky gabim duhet të shpërfillet, çaktivizoni  `jo-matching-header`  check in  {validator}. Kufizimi i modelit Skema e ofruar nuk është e vlefshme.

  Si mund të zgjidhet:
  - Përditëso përshkrimin e skemës të jetë një përshkrim i vlefshëm
  - Nëse ky gabim duhet të injorohet, çaktivizoni kontrollimin e skemës në {validator}. Kufizimi i kërkuar Burimi nuk u gjet. Rreshti {row_number} ka një vlerë që mungon në kolonën {column_number} Rreshti {row_number} ka një vlerë shtesë në kolonën {column_number} Rreshti {row_number} është tërësisht i paplotësuar Rreshti {row_number} është i dubluar në rreshtin {row_numbers} Rreshtat {row_numbers} kanë shkelje të kufizimeve unike në kolonën {column_number} Skemë e gabuar Shfaq 10 rreshtat e ardhshëm Burim i gabuar Detajet e suksesit Gabim i skemës së tabelës Gabim i skemës së tabelës: {error_message} Inspektimi i tabelës ka arritur një kufi prej 1000 rreshtave Burimi i të dhënave nuk mund të dekodohej me sukses me {encoding} kodimin Burimi i të dhënave nuk ka mbështetje ose ka përmbajtje të paqëndrueshme; nuk mund të nxirren të dhëna tabelare Burimi i të dhënave është në një format të panjohur; nuk mund të nxirren të dhëna tabelare Burimi i të dhënave është në një skemë të panjohur; nuk mund të nxirren të dhëna tabelare Burimi i të dhënave ka rikthyer një gabim HTTP me kodin e statusit të {status_code} Burimi i të dhënave ka rikthyer një Gabim IO të llojit {error_type} Të dhënat e njëjta të sakta janë parë në një rresht tjetër.

  Si mund të zgjidhet:
  - Nëse disa nga të dhënat janë të pasakta, korrigjoni ato.
  - Nëse i tërë rreshti është një dublim i pasaktë, hiqeni atë.
  - Nëse ky gabim duhet të injorohet, çaktivizoni në 'double-row` check in {validator}. Rreshti i parë i burimit të të dhënave përmban titull i cili nuk ekziston në skemë.

  Si mund të zgjidhet:
  - Hiqni kolonën shtesë nga burimi i të dhënave ose shtoni fushën që mungon në skemën
  - Nëse ky gabim duhet të injorohet, çaktivizoni `extra-header` kontrollo në {validator}. Lista e plotë e mesazheve të gabimit: Vlera nuk përputhet me llojin dhe formatin e skemës për këtë fushë.

  Si mund të zgjidhet:
  - Nëse kjo vlerë nuk është e saktë, përditësoni vlerën.
  - Nëse kjo vlerë është e saktë, rregulloni llojin dhe/ose formatin.
  - Për ta injoruar gabimin, çaktivizoni `type-or-format-error` check-in {validator}. Në këtë rast të gjitha kontrollet e skemës për vlerat e rreshtit do të injorohen. Vlera {vlera} në rresht {row_number} dhe kolona {column_number} nuk përputhet me numërimin e dhënë: {constraint} Vlera {vlera} në rresht {row_number} dhe kolona {column_number} nuk përputhet me kufizimet maksimale të {constraint} Vlera {vlera} në rresht {row_number} dhe kolona {column_number} nuk përputhet me kufizimin maksimal të gjatësisë së {constraint} Vlera {vlera} në rresht {row_number} dhe kolona {column_number} nuk përputhet me kufizimet minimale të {constraint} Vlera {vlera} në rresht {row_number} dhe kolona {column_number} nuk përputhet me kufizimin minimal të gjatësisë së {constraint} Vlera {vlera} në rresht {row_number} dhe kolona {column_number} nuk përputhet me kufizimet e modelit të {constraint} Vlera {vlera} në rresht {row_number} dhe kolona {column_number} nuk është lloji {field_type} dhe formati {field_format} Ka  Ka një titull që mungon në kolonën {column_number} Ekziston një titull shtesë në kolonën {column_number} Kjo fushë është një fushë e kërkuar, por nuk përmban asnjë vlerë.

  Si mund të zgjidhet:
  - Nëse kjo vlerë nuk është e saktë, përditësoni vlerën.
  - Nëse vlera është e saktë, atëherë hiqni nga skema kufizimin 'required'.
  - Nëse ky gabim duhet të injorohet, çaktivizoni 'kufizimet e kërkuara' në {validator}. Kjo fushë është një fushë unike por përmban një vlerë që është përdorur në një rresht tjetër.

  Si mund të zgjidhet:
  - Nëse kjo vlerë nuk është e saktë, përditësoni vlerën.
  - Nëse vlera është e saktë, atëherë vlerat në këtë kolonë nuk janë unike. Hiqni detyrimin "unique" nga skema.
  - Nëse ky gabim duhet të injorohet, çaktivizoni `unique-constraint` check in {validator}. Kjo vlerë në fushë duhet të jetë e barabartë me një nga vlerat në kufizimet e regjistrimit.

  Si mund të zgjidhet:
  - Nëse kjo vlerë nuk është e saktë, përditësoni vlerën.
  - Nëse vlera është e saktë, atëherë hiqni ose përmirësoni kufizimin `enum` në skemë.
  - Nëse ky gabim duhet të shpërfillet, çaktivizoni `enumerable-constraint` check in {validator}. Kjo vlerë e fushës duhet të jetë më e madhe ose e barabartë sesa vlera kufizuese.

  Si mund të zgjidhet:
  - Nëse kjo vlerë nuk është e saktë, përditësoni vlerën.
  - Nëse vlera është e saktë, atëherë hiqni ose përsosni kufizimet 'minimum' në skemë.
  - Nëse ky gabim duhet të injorohet, çaktivizoni 'minimum-constraint` check in {validator}. Kjo vlerë e fushës duhet të jetë më pak ose e barabartë sesa vlera kufizuese.

  Si mund të zgjidhet:
  - Nëse kjo vlerë nuk është e saktë, përditësoni vlerën.
  - Nëse vlera është e saktë, atëherë hiqni ose përsosni kufizimet 'maximum' në skemë.
  - Nëse ky gabim duhet të injorohet, çaktivizoni `maximum-constraint` check in {validator}. Kjo vlerë e fushës duhet të jetë në përputhje me modelin e kufizimit.

  Si mund të zgjidhet:
  - Nëse kjo vlerë nuk është e saktë, përditësoni vlerën.
  - Nëse vlera është e saktë, atëherë hiqni ose përmirësoni kufizimet  `pattern` në skemë.
  - Nëse ky gabim duhet të injorohet, çaktivizoni `constraint pattern` check in {validator}. Ky rresht ka më pak vlera krahasuar me fillimin e rreshtit (rreshti i parë në burimin e të dhënave). Një koncept kryesor është se të gjitha rreshtat në të dhënat tabelare duhet të kenë të njëjtin numër kolonash.
  Si mund të zgjidhet:
  - Kontrollo të dhënat, nuk mungon një presje ndërmjet vlerave në këtë rresht.
  - Nëse ky gabim duhet të injorohet,çaktivizoni missing-value` check in {validator}. Ky rresht ka më shumë vlera krahasuar me fillimin e rreshtit (rreshti i parë në burimin e të dhënave). Një koncept kryesor është se të gjitha rreshtat në të dhënat tabelare duhet të kenë të njëjtin numër kolonash.
Si mund të zgjidhet:
  - Kontrollo të dhënat, ka një presje shtesë ndërmjet vlerave në këtë rresht.
  - Nëse ky gabim duhet të injorohet, çaktivizoni tek `extra-value` check in {validator}. Ky rresht është i paplotësuar. Një rresht duhet të përmbajë të paktën një vlerë.

  Si mund të zgjidhet:
  - Fshi rreshtin.
  - Nëse ky gabim duhet të injorohet, çaktivizoni 'blank-row` check in {validator}. Dy kolona në fillimin e rreshtit kanë të njëjtën vlerë. Emrat e kolonës duhet të jenë unike.

  Si mund të zgjidhet:
 - Shto emrin e kolonës që mungon në rreshtin e parë të të dhënave.
 - Nëse fillon rreshti i parë ose përfundon me presje, hiqeni atë.
 - Nëse ky gabim duhet të injorohet, çaktivizo `blank-header` check in {validator}. Lloji ose Formati Gabim URL-ja për skedarin e skemës së të dhënave e disponueshme në internet I paautorizuar për të lexuar këtë raport validimi Kufizim unik Ngarkoni Ngarko një skedar të skemës së të dhënave nga kompjuteri yt Skema e të dhënave të ngarkuara Të dhënat e vlefshme Raporti i Validimit Vlefshmëria e validimit Detajet e paralajmërimit të dhëna gabim dështim I pavlefshëm Skema Strukturë sukses i panjohur 