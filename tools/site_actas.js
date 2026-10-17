/* =====================================================================
   Actas de reunión — editor en línea, almacenamiento y exportación.
   Esquema: dist/acta.schema.json. Formato Word: espejo de tools/acta.py.
   ===================================================================== */
const ACTAS=DATA.actas;                       // catálogo de tipos (catalogo/actas.yaml)
const TIPO=Object.fromEntries(ACTAS.tipos.map(t=>[t.id,t]));
const EST_DEC=["Acordada","Pendiente de aprobación","Rechazada"],EST_ACU=["Abierto","Cerrado"],EST_CONF=["Pendiente","Conforme","Observado"];
const MODALIDADES=["Presencial","Virtual","Mixta"];
const ROLES=ACTAS.roles;

/* ---------------- almacenamiento: db compartida en línea, o este navegador */
const AStore={mode:"cargando",db:null,user:null,me:null,canWrite:true,docs:new Map(),subs:new Set(),dl:null,saving:new Map(),
  async init(){
    if(this._init)return this._init;
    this._init=(async()=>{
      const C=window.claude;
      const db=C&&C.use?await C.use("db").catch(()=>null):null;
      this.user=C&&C.use?await C.use("user").catch(()=>null):null;
      this.dl=C&&C.use?await C.use("downloads").catch(()=>null):null;
      if(this.user){this.me=await this.user.id();const w=await this.user.can("data.write");this.canWrite=w!==false}
      if(db){this.db=db;this.mode="linea";
        db.collection("actas").orderBy("actualizado","desc").limit(500).onSnapshot(s=>{
          this.docs=new Map(s.docs.map(d=>[d.id,{...d.data(),id:d.id}]));this.emit()},
          e=>{this.mode="error";this.err=e.code;this.emit()});
      }else{this.mode="local";
        try{(JSON.parse(localStorage.getItem("actas.local")||"[]")).forEach(a=>this.docs.set(a.id,a))}catch(e){}
        this.emit()}
    })();
    return this._init;
  },
  emit(){this.subs.forEach(f=>f())},
  list(){return [...this.docs.values()].sort((a,b)=>(b.actualizado||"").localeCompare(a.actualizado||""))},
  async save(a){
    a.actualizado=new Date().toISOString();a.actualizado_por=this.me;
    const body=JSON.parse(JSON.stringify(a));delete body.id;
    if(this.mode==="linea"){
      // una escritura a la vez por documento; la última versión pendiente gana
      const q=this.saving.get(a.id);if(q){q.next=body;return q.p}
      const run=async(b)=>{try{await this.db.doc("actas/"+a.id).set(b)}finally{
        const s=this.saving.get(a.id);if(s&&s.next){const n=s.next;s.next=null;s.p=run(n);return s.p}this.saving.delete(a.id)}};
      const st={next:null};st.p=run(body);this.saving.set(a.id,st);return st.p;
    }
    this.docs.set(a.id,{...body,id:a.id});
    try{localStorage.setItem("actas.local",JSON.stringify([...this.docs.values()]))}catch(e){throw {code:"local_full"}}
    this.emit();
  },
  async remove(id){
    if(this.mode==="linea")return this.db.doc("actas/"+id).delete();
    this.docs.delete(id);try{localStorage.setItem("actas.local",JSON.stringify([...this.docs.values()]))}catch(e){}this.emit();
  },
  async names(ids){
    ids=[...new Set(ids.filter(Boolean))];if(!this.user||!ids.length)return {};
    try{return await this.user.profiles(ids)}catch(e){return {}}
  }
};
const newId=()=>"a-"+Date.now().toString(36)+"-"+Math.random().toString(36).slice(2,7);
const hoy=()=>new Date().toISOString().slice(0,10);

function actaNueva(t,m,n){
  return {id:newId(),tipo:t.id,numero:`ACTA-${m.codigo}-${String(n).padStart(2,"0")}`,estado:"Borrador",version:1,
    modelo:{codigo:m.codigo,nombre:m.nombre,tier:m.tier||"",tipo_modelo:m.tipo_modelo||""},
    fecha:m.fecha||hoy(),hora_inicio:"",hora_fin:"",modalidad:"Virtual",lugar:"",secretario:"",
    objetivo:t.objetivo||"",agenda:[...(t.agenda||[])],resumen:"",
    asistentes:t.participantes.map(p=>({nombre:"",area:p.area,rol:p.rol,asistio:true})),
    decisiones:t.decisiones.map(d=>({texto:d.texto,ref:d.ref||"",responsable:"",estado:"Pendiente de aprobación"})),
    excepciones:[],acuerdos:[],evidencias:[...(t.entregables||[])],
    conformidad:t.participantes.filter(p=>p.rol==="Decide"||p.rol==="Aprueba").map(p=>({nombre:"",area:p.area,estado:"Pendiente",fecha:"",medio:"Correo"})),
    historial:[{fecha:new Date().toISOString(),version:1,cambio:"Creación del acta",por:AStore.me}],
    creado:new Date().toISOString(),creado_por:AStore.me,estandar_version:DATA.meta.version};
}
function validarActa(a){
  const e=[];
  if(!a.modelo.codigo||!a.modelo.nombre)e.push("Completa el código y el nombre del modelo.");
  if(!a.fecha)e.push("Indica la fecha de la reunión.");
  if(!a.resumen.trim())e.push("Escribe el desarrollo de la reunión (sección 5).");
  if(a.asistentes.some(x=>!x.nombre.trim()))e.push("Hay participantes sin nombre (sección 2).");
  if(!a.conformidad.length)e.push("Agrega al menos un aprobador (sección 10).");
  if(a.conformidad.some(c=>c.estado!=="Conforme"))e.push("Todos los aprobadores deben estar en «Conforme» (sección 10).");
  if(a.decisiones.some(d=>d.estado==="Pendiente de aprobación"))e.push("Hay decisiones aún «Pendiente de aprobación» (sección 6).");
  return e;
}

/* ---------------- Markdown */
const MOD_LBL={lineal:"Lineal",ml:"ML",arbol:"Árbol",acp:"ACP"};
const cell=s=>String(s??"").replace(/\|/g,"\\|").replace(/\n/g,"<br>")||"—";
function actaMd(a){
  const t=TIPO[a.tipo]||{},m=a.modelo,L=[];
  L.push(`# Acta de reunión · ${a.numero}`,"",`**${t.nombre||a.tipo}** · Estado: **${a.estado}** · Versión ${a.version}${t.requisito?` · Requisito del estándar: \`${t.requisito}\``:""}`,"",
    "## 1. Datos generales","","| | | | |","|---|---|---|---|",
    `| **Código de modelo** | ${cell(m.codigo)} | **Nombre del modelo** | ${cell(m.nombre)} |`,
    `| **Tier** | ${cell(m.tier)} | **Tipo de modelo** | ${cell(MOD_LBL[m.tipo_modelo])} |`,
    `| **Fecha** | ${cell(a.fecha)} | **Horario** | ${a.hora_inicio||"—"} – ${a.hora_fin||"—"} |`,
    `| **Modalidad** | ${cell(a.modalidad)} | **Lugar / enlace** | ${cell(a.lugar)} |`,
    `| **Secretario** | ${cell(a.secretario)} | **Hito** | ${cell(t.acta)} |`,"",
    "## 2. Participantes","","| Nombre | Área | Rol | Asistió |","|---|---|---|---|",
    ...a.asistentes.map(x=>`| ${cell(x.nombre)} | ${cell(x.area)} | ${cell(x.rol)} | ${x.asistio?"Sí":"No"} |`),"",
    "## 3. Objetivo","",a.objetivo||"—","","## 4. Agenda","",...(a.agenda.length?a.agenda.map((x,i)=>`${i+1}. ${x}`):["—"]),"",
    "## 5. Desarrollo de la reunión","",a.resumen||"—","","## 6. Decisiones","");
  if(a.decisiones.length)L.push("| # | Decisión | Requisito | Responsable | Estado |","|---|---|---|---|---|",...a.decisiones.map((d,i)=>`| ${i+1} | ${cell(d.texto)} | ${cell(d.ref)} | ${cell(d.responsable)} | ${d.estado} |`));else L.push("Sin decisiones registradas.");
  L.push("","## 7. Excepciones a umbrales","");
  if(a.excepciones.length)L.push("| Umbral | Valor obtenido | Justificación | ¿Va a Comité? |","|---|---|---|---|",...a.excepciones.map(e=>`| ${cell(e.umbral)} | ${cell(e.valor)} | ${cell(e.justificacion)} | ${e.comite?"Sí":"No"} |`));else L.push("No se registraron excepciones.");
  L.push("","## 8. Acuerdos y pendientes","");
  if(a.acuerdos.length)L.push("| # | Acción | Responsable | Fecha compromiso | Estado |","|---|---|---|---|---|",...a.acuerdos.map((x,i)=>`| ${i+1} | ${cell(x.accion)} | ${cell(x.responsable)} | ${cell(x.fecha)} | ${x.estado} |`));else L.push("Sin pendientes.");
  L.push("","## 9. Evidencias y entregables revisados","",...(a.evidencias.length?a.evidencias.map(x=>"- "+x):["—"]),"",
    "## 10. Conformidad","","| Nombre | Área / cargo | Conformidad | Fecha | Medio |","|---|---|---|---|---|",
    ...a.conformidad.map(c=>`| ${cell(c.nombre)} | ${cell(c.area)} | ${c.estado} | ${cell(c.fecha)} | ${cell(c.medio)} |`),"",
    "## 11. Control de cambios","","| Versión | Fecha | Cambio |","|---|---|---|",...a.historial.map(h=>`| ${h.version} | ${String(h.fecha).slice(0,10)} | ${cell(h.cambio)} |`),"",
    "---",`*${DATA.meta.nombre} v${a.estandar_version||DATA.meta.version} · ${DATA.meta.custodio}*`,"");
  return L.join("\n");
}

/* ---------------- Word (.docx, OOXML) — espejo de tools/acta.py */
const X=s=>String(s??"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
const C_INK="1B2A2F",C_SEAL="7A2632",C_MUTED="4A5A60",C_RULE="C9D1CE",C_WASH="EAEFEC";
const wr=(text,o={})=>{const rpr=(o.b?"<w:b/>":"")+(o.i?"<w:i/>":"")+(o.color?`<w:color w:val="${o.color}"/>`:"")+(o.sz?`<w:sz w:val="${o.sz}"/><w:szCs w:val="${o.sz}"/>`:"");
  return `<w:r>${rpr?"<w:rPr>"+rpr+"</w:rPr>":""}${String(text??"").split("\n").map(p=>`<w:t xml:space="preserve">${X(p)}</w:t>`).join("<w:br/>")}</w:r>`};
const wp=(runs,o={})=>{const ppr=(o.style?`<w:pStyle w:val="${o.style}"/>`:"")+(o.keep?"<w:keepNext/>":"")+(o.after!=null?`<w:spacing w:after="${o.after}"/>`:"");
  if(typeof runs==="string"&&!runs.startsWith("<w:r"))runs=runs?wr(runs):"";return `<w:p>${ppr?"<w:pPr>"+ppr+"</w:pPr>":""}${runs}</w:p>`};
const wtc=(c,w,o={})=>`<w:tc><w:tcPr><w:tcW w:w="${w}" w:type="dxa"/>${o.fill?`<w:shd w:val="clear" w:color="auto" w:fill="${o.fill}"/>`:""}</w:tcPr>${wp(wr(c,{b:o.b,color:o.color}),{after:0})}</w:tc>`;
function wtbl(rows,widths,o={}){const header=o.header!==false,lab=o.label||[];const b=`w:val="single" w:sz="4" w:space="0" w:color="${C_RULE}"`;
  let s=`<w:tbl><w:tblPr><w:tblW w:w="${widths.reduce((x,y)=>x+y,0)}" w:type="dxa"/><w:tblBorders><w:top ${b}/><w:left ${b}/><w:bottom ${b}/><w:right ${b}/><w:insideH ${b}/><w:insideV ${b}/></w:tblBorders><w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>${widths.map(w=>`<w:gridCol w:w="${w}"/>`).join("")}</w:tblGrid>`;
  rows.forEach((row,ri)=>{const hdr=header&&ri===0;s+=`<w:tr>${hdr?"<w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>":"<w:trPr><w:cantSplit/></w:trPr>"}`+
    row.map((c,ci)=>{const L=hdr||lab.includes(ci);return wtc(c===""||c==null?"—":c,widths[ci],{fill:L?C_WASH:null,b:L,color:L?C_INK:null})}).join("")+"</w:tr>"});
  return s+"</w:tbl>"+wp("",{after:120})}
const wh=(n,t)=>wp(wr(`${n}. ${t}`),{style:"Heading1",keep:true});
async function actaDocx(a){
  const t=TIPO[a.tipo]||{},m=a.modelo,W=9638;
  const body=[
    wp(wr("ACTA DE REUNIÓN",{b:true,color:C_SEAL,sz:18}),{after:40}),
    wp(wr(t.nombre||a.tipo),{style:"Title"}),
    wp(wr(`${a.numero}  ·  Estado: `,{color:C_MUTED})+wr(a.estado,{b:true,color:a.estado==="Aprobada"?C_SEAL:C_INK})+wr(`  ·  Versión ${a.version}${t.requisito?"  ·  Requisito "+t.requisito:""}`,{color:C_MUTED}),{after:240}),
    wh(1,"Datos generales"),
    wtbl([["Código de modelo",m.codigo,"Nombre del modelo",m.nombre],["Tier",m.tier,"Tipo de modelo",MOD_LBL[m.tipo_modelo]||""],
      ["Fecha",a.fecha,"Horario",`${a.hora_inicio||"—"} – ${a.hora_fin||"—"}`],["Modalidad",a.modalidad,"Lugar / enlace",a.lugar],
      ["Secretario",a.secretario,"Hito del estándar",t.acta]],[1900,2919,1900,2919],{header:false,label:[0,2]}),
    wh(2,"Participantes"),
    wtbl([["Nombre","Área","Rol","Asistió"],...a.asistentes.map(x=>[x.nombre,x.area,x.rol,x.asistio?"Sí":"No"])],[3200,3338,1900,1200]),
    wh(3,"Objetivo"),wp(a.objetivo||"—",{after:160}),
    wh(4,"Agenda"),...a.agenda.map((x,i)=>wp(wr(`${i+1}.  `,{b:true,color:C_SEAL})+wr(x),{after:40})),wp("",{after:80}),
    wh(5,"Desarrollo de la reunión"),...(a.resumen||"—").split("\n\n").map(p=>wp(p,{after:120})),
    wh(6,"Decisiones"),
    a.decisiones.length?wtbl([["#","Decisión","Requisito","Responsable","Estado"],...a.decisiones.map((d,i)=>[String(i+1),d.texto,d.ref,d.responsable,d.estado])],[450,4100,1700,1800,1588])
      :wtbl([["#","Decisión"],["—","Sin decisiones registradas"]],[450,9188]),
    wh(7,"Excepciones a umbrales"),
    a.excepciones.length?wtbl([["Umbral","Valor obtenido","Justificación","¿Va a Comité?"],...a.excepciones.map(e=>[e.umbral,e.valor,e.justificacion,e.comite?"Sí":"No"])],[1300,1900,5038,1400])
      :wp(wr("No se registraron excepciones.",{i:true,color:C_MUTED}),{after:160}),
    wh(8,"Acuerdos y pendientes"),
    a.acuerdos.length?wtbl([["#","Acción","Responsable","Fecha compromiso","Estado"],...a.acuerdos.map((x,i)=>[String(i+1),x.accion,x.responsable,x.fecha,x.estado])],[450,4500,2000,1588,1100])
      :wp(wr("Sin pendientes.",{i:true,color:C_MUTED}),{after:160}),
    wh(9,"Evidencias y entregables revisados"),...(a.evidencias.length?a.evidencias.map(x=>wp(wr("▪  ",{color:C_SEAL})+wr(x),{after:40})):[wp("—")]),wp("",{after:80}),
    wh(10,"Conformidad"),
    wtbl([["Nombre","Área / cargo","Conformidad","Fecha","Medio","Firma"],...a.conformidad.map(c=>[c.nombre,c.area,c.estado,c.fecha,c.medio," "])],[2000,2200,1300,1200,1100,1838]),
    wh(11,"Control de cambios"),
    wtbl([["Versión","Fecha","Cambio"],...a.historial.map(h=>[String(h.version),String(h.fecha).slice(0,10),h.cambio])],[1000,1600,7038])];
  const NS='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"';
  const XH='<?xml version="1.0" encoding="UTF-8" standalone="yes"?>';
  const sect='<w:sectPr><w:headerReference w:type="default" r:id="rIdH"/><w:footerReference w:type="default" r:id="rIdF"/><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1418" w:right="1134" w:bottom="1247" w:left="1134" w:header="567" w:footer="567" w:gutter="0"/></w:sectPr>';
  const fr=`<w:rPr><w:color w:val="${C_MUTED}"/><w:sz w:val="16"/></w:rPr>`;
  const fld=c=>`<w:r>${fr}<w:fldChar w:fldCharType="begin"/></w:r><w:r>${fr}<w:instrText xml:space="preserve"> ${c} </w:instrText></w:r><w:r>${fr}<w:fldChar w:fldCharType="separate"/></w:r><w:r>${fr}<w:t>1</w:t></w:r><w:r>${fr}<w:fldChar w:fldCharType="end"/></w:r>`;
  const files={
    "[Content_Types].xml":XH+'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/><Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/><Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>',
    "_rels/.rels":XH+'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>',
    "word/_rels/document.xml.rels":XH+'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rIdT" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/><Relationship Id="rIdH" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/><Relationship Id="rIdF" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>',
    "word/document.xml":XH+`<w:document ${NS}><w:body>${body.join("")}${sect}</w:body></w:document>`,
    "word/styles.xml":XH+`<w:styles ${NS}><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/><w:color w:val="${C_INK}"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="es-PE"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="80" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="60"/></w:pPr><w:rPr><w:rFonts w:ascii="Georgia" w:hAnsi="Georgia"/><w:color w:val="${C_INK}"/><w:sz w:val="40"/><w:szCs w:val="40"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="2" w:color="${C_RULE}"/></w:pBdr><w:spacing w:before="280" w:after="100"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:rFonts w:ascii="Georgia" w:hAnsi="Georgia"/><w:b/><w:color w:val="${C_SEAL}"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style></w:styles>`,
    "word/settings.xml":XH+`<w:settings ${NS}><w:defaultTabStop w:val="709"/></w:settings>`,
    "word/header1.xml":XH+`<w:hdr ${NS}><w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="${C_SEAL}"/></w:pBdr><w:tabs><w:tab w:val="right" w:pos="${W}"/></w:tabs></w:pPr>${wr(DATA.meta.nombre.toUpperCase(),{b:true,color:C_SEAL,sz:16})}<w:r><w:tab/></w:r>${wr(`${a.numero}  ·  ${m.codigo}`,{color:C_MUTED,sz:16})}</w:p></w:hdr>`,
    "word/footer1.xml":XH+`<w:ftr ${NS}><w:p><w:pPr><w:pBdr><w:top w:val="single" w:sz="4" w:space="4" w:color="${C_RULE}"/></w:pBdr><w:tabs><w:tab w:val="right" w:pos="${W}"/></w:tabs></w:pPr>${wr(DATA.meta.custodio,{b:true,color:C_INK,sz:16})}${wr("  ·  Uso interno",{color:C_MUTED,sz:16})}<w:r><w:tab/></w:r>${wr("Página ",{color:C_MUTED,sz:16})}${fld("PAGE")}${wr(" de ",{color:C_MUTED,sz:16})}${fld("NUMPAGES")}</w:p></w:ftr>`,
    "docProps/core.xml":XH+`<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>${X(a.numero+" · "+(t.nombre||""))}</dc:title><dc:subject>${X(m.codigo+" · "+m.nombre)}</dc:subject><dc:creator>${X(DATA.meta.nombre)}</dc:creator><cp:keywords>acta; ${X(a.tipo)}; ${X(m.codigo)}</cp:keywords><dcterms:created xsi:type="dcterms:W3CDTF">${new Date().toISOString().slice(0,19)}Z</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">${new Date().toISOString().slice(0,19)}Z</dcterms:modified></cp:coreProperties>`,
    "docProps/app.xml":XH+`<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>${X(DATA.meta.nombre)}</Application><Company>${X(DATA.meta.custodio)}</Company></Properties>`};
  const zip=new JSZip();for(const [k,v] of Object.entries(files))zip.file(k,v);
  return zip.generateAsync({type:"blob",compression:"DEFLATE",mimeType:"application/vnd.openxmlformats-officedocument.wordprocessingml.document"});
}
async function ofrecerArchivo(filename,data,note){
  try{
    if(AStore.dl){await AStore.dl.save({filename,data});note("Archivo listo: "+filename);return}
    if(window.claude&&window.claude.use){note("La descarga no está disponible en esta vista. Usa «Copiar Markdown».");return}
    const blob=data instanceof Blob?data:new Blob([data],{type:"text/markdown"});const u=URL.createObjectURL(blob);
    const l=document.createElement("a");l.href=u;l.download=filename;document.body.append(l);l.click();l.remove();setTimeout(()=>URL.revokeObjectURL(u),4000);note("Archivo descargado: "+filename);
  }catch(e){note(e&&e.code==="declined"?"Descarga cancelada.":e&&e.code==="rate_limited"?"Ya hay una descarga pendiente de confirmar.":"No se pudo preparar la descarga.")}
}
const fileBase=a=>`${a.numero}_${(TIPO[a.tipo]||{}).id||a.tipo}`.replace(/[^\w.-]+/g,"_");

/* ---------------- vistas */
const chipEstado=e=>`<span class="chip est-${e==="Aprobada"?"ok":e==="En revisión"?"rev":"bor"}">${esc(e)}</span>`;
const fmtFecha=s=>s?new Date(s).toLocaleString("es-PE",{dateStyle:"medium",timeStyle:"short"}):"—";
let actasFiltro=store.get("actas.filtro",{q:"",estado:""});

function modoTxt(){return AStore.mode==="linea"?(AStore.canWrite?"Guardado en línea · visible para el equipo":"Solo lectura: tu acceso no permite editar"):
  AStore.mode==="local"?"Guardado en este navegador (sin conexión al espacio compartido)":AStore.mode==="error"?"No se pudo conectar con el espacio compartido":"Conectando…"}

async function showActas(){
  await AStore.init();
  const render=()=>{
    if(currentView!=="actas")return;
    const all=AStore.list();const q=actasFiltro.q.toLowerCase();
    const rows=all.filter(a=>(!actasFiltro.estado||a.estado===actasFiltro.estado)&&(!q||(a.numero+" "+a.modelo.codigo+" "+a.modelo.nombre+" "+(TIPO[a.tipo]||{}).nombre).toLowerCase().includes(q)));
    const cnt=e=>all.filter(a=>a.estado===e).length;
    $("#view").innerHTML=`<div class="wide actas">
      <div class="plan-head"><h1>Actas de reunión</h1><p>Cada hito del estándar deja un acta. Créala desde su tipo y se precargan objetivo, agenda, decisiones con su requisito, entregables y aprobadores. Se guarda sola, pasa por revisión y, al aprobarse, queda bloqueada con su historial. Se descarga en Word o Markdown.</p></div>
      <div class="a-bar"><span class="a-mode m-${AStore.mode}">${esc(modoTxt())}</span>
        <div class="a-bar-r"><button type="button" id="aEjemplo">Ver un ejemplo</button>${AStore.canWrite?`<button type="button" class="primary" id="aNueva">Nueva acta</button>`:""}</div></div>
      <div id="aNuevaPanel"></div>
      <div class="summary s3"><div><b>${cnt("Borrador")}</b><span>en borrador</span></div><div><b>${cnt("En revisión")}</b><span>en revisión</span></div><div><b>${cnt("Aprobada")}</b><span>aprobadas</span></div></div>
      <div class="a-filtros"><label for="aQ" class="sr">Buscar acta</label><input id="aQ" type="search" placeholder="Buscar por N°, código o nombre de modelo" value="${esc(actasFiltro.q)}">
        <label for="aEst" class="sr">Estado</label><select id="aEst"><option value="">Todos los estados</option>${ACTAS.estados.map(e=>`<option ${actasFiltro.estado===e?"selected":""}>${e}</option>`).join("")}</select></div>
      ${all.length===0?`<div class="a-empty"><h2>Aún no hay actas</h2><p>Empieza con <b>Nueva acta</b>: elige el hito (por ejemplo, <i>Reunión 5 · Selección del modelo final</i>), indica el código del modelo y el acta se arma con lo que el estándar exige para esa reunión. Si prefieres ver cómo queda, abre <b>Ver un ejemplo</b>.</p></div>`:
      rows.length===0?`<p class="a-none">Ninguna acta coincide con el filtro.</p>`:
      `<div class="tbl"><table class="a-list"><thead><tr><th>N° de acta</th><th>Reunión</th><th>Modelo</th><th>Fecha</th><th>Estado</th><th>Última edición</th></tr></thead><tbody>
      ${rows.map(a=>`<tr data-open="${esc(a.id)}" tabindex="0"><td class="mono">${esc(a.numero)}</td><td>${esc((TIPO[a.tipo]||{}).nombre||a.tipo)}</td><td><span class="mono">${esc(a.modelo.codigo)}</span><br><small>${esc(a.modelo.nombre)}</small></td><td class="mono">${esc(a.fecha)}</td><td>${chipEstado(a.estado)} <small>v${a.version}</small></td><td><small>${esc(fmtFecha(a.actualizado))}</small></td></tr>`).join("")}
      </tbody></table></div>`}
    </div>`;
    $("#aQ")&&($("#aQ").oninput=e=>{actasFiltro.q=e.target.value;store.set("actas.filtro",actasFiltro);clearTimeout(render.t);render.t=setTimeout(()=>{render();const i=$("#aQ");i.focus();i.setSelectionRange(i.value.length,i.value.length)},200)});
    $("#aEst")&&($("#aEst").onchange=e=>{actasFiltro.estado=e.target.value;store.set("actas.filtro",actasFiltro);render()});
    $("#aNueva")&&($("#aNueva").onclick=panelNueva);
    $("#aEjemplo").onclick=()=>openActa(ejemplo(),true);
    $("#view").querySelectorAll("tr[data-open]").forEach(tr=>{const go=()=>{location.hash="#"+tr.dataset.open};tr.onclick=go;tr.onkeydown=e=>{if(e.key==="Enter")go()}});
  };
  AStore.subs.clear();AStore.subs.add(render);render();
}

function panelNueva(){
  const last=AStore.list()[0];
  const grupos=["Gobierno","Desarrollo","Calibración","Implementación","Parámetros","Pricing"];
  $("#aNuevaPanel").innerHTML=`<form class="a-new" id="aNewForm">
    <h2>Nueva acta</h2>
    <div class="a-grid">
      <label class="ctl full" for="nTipo"><span>Reunión / hito del estándar</span><select id="nTipo" required>${grupos.map(g=>`<optgroup label="${g}">${ACTAS.tipos.filter(t=>t.estandar===g).map(t=>`<option value="${t.id}">${esc(t.nombre)} — ${esc(t.acta)}</option>`).join("")}</optgroup>`).join("")}</select></label>
      <label class="ctl" for="nCod"><span>Código de modelo</span><input id="nCod" required placeholder="MOD-ORI-001" value="${esc(last?last.modelo.codigo:"")}"></label>
      <label class="ctl" for="nNom"><span>Nombre del modelo</span><input id="nNom" required placeholder="Score de originación TC" value="${esc(last?last.modelo.nombre:"")}"></label>
      <label class="ctl" for="nTier"><span>Tier</span><select id="nTier">${["","I","II","III","IV"].map(x=>`<option ${last&&last.modelo.tier===x?"selected":""}>${x}</option>`).join("")}</select></label>
      <label class="ctl" for="nMod"><span>Tipo de modelo</span><select id="nMod"><option value=""></option>${Object.entries(MOD_LBL).map(([k,v])=>`<option value="${k}" ${last&&last.modelo.tipo_modelo===k?"selected":""}>${v}</option>`).join("")}</select></label>
      <label class="ctl" for="nFecha"><span>Fecha de la reunión</span><input id="nFecha" type="date" required value="${hoy()}"></label>
    </div>
    <p class="a-hint" id="nHint"></p>
    <div class="a-actions"><button class="primary" type="submit">Crear acta</button><button type="button" id="nCancel">Cancelar</button></div></form>`;
  const hint=()=>{const t=TIPO[$("#nTipo").value];$("#nHint").innerHTML=`Se precargan ${t.agenda.length} puntos de agenda, ${t.decisiones.length} decisiones esperadas y ${t.participantes.length} roles${t.requisito?`. Requisito del estándar: <a class="rid" href="#" data-id="${t.requisito}">${t.requisito}</a>`:""}.`};
  $("#nTipo").onchange=hint;hint();$("#nTipo").focus();
  $("#nCancel").onclick=()=>{$("#aNuevaPanel").innerHTML=""};
  $("#aNewForm").onsubmit=async e=>{e.preventDefault();
    const m={codigo:$("#nCod").value.trim(),nombre:$("#nNom").value.trim(),tier:$("#nTier").value,tipo_modelo:$("#nMod").value,fecha:$("#nFecha").value};
    const n=AStore.list().filter(a=>a.modelo.codigo===m.codigo).length+1;
    const a=actaNueva(TIPO[$("#nTipo").value],m,n);
    try{await AStore.save(a);location.hash="#"+a.id}catch(err){$("#nHint").textContent=err&&err.code==="quota_exceeded"?"El espacio de actas está lleno. Elimina actas que ya no se usen.":"No se pudo crear el acta. Revisa tu conexión e inténtalo de nuevo."}};
}

function ejemplo(){
  const a=actaNueva(TIPO.R5,{codigo:"MOD-EJEMPLO-001",nombre:"Score de originación — ejemplo",tier:"II",tipo_modelo:"ml",fecha:hoy()},5);
  a.id="ejemplo";a.numero="ACTA-EJEMPLO-05";a.hora_inicio="10:00";a.hora_fin="11:15";a.lugar="Sala virtual del equipo";a.secretario="Analista de modelos (ejemplo)";
  a.asistentes=[{nombre:"Gerente de producto (ejemplo)",area:"Negocio / banca usuaria",rol:"Decide",asistio:true},{nombre:"Jefe de modelos (ejemplo)",area:"Jefatura de modelos",rol:"Aprueba",asistio:true},{nombre:"Analista de modelos (ejemplo)",area:"Equipo de modelos",rol:"Secretario",asistio:true}];
  a.resumen="Se presentaron tres modelos candidatos (XGBoost, LightGBM y logística WOE como benchmark). El XGBoost obtuvo Gini OOT de 52.1 frente a 54.0 en Train (diferencia de 1.9 pts, dentro de U-11) y supera al modelo vigente en 6.4 pts en las cosechas aprobadas de los últimos seis meses.\n\nNegocio revisó el sentido económico de las 24 variables finales; se pidió retirar una variable de canal por riesgo de sesgo operativo.";
  a.decisiones=a.decisiones.map((d,i)=>({...d,responsable:i===0?"Gerente de producto (ejemplo)":"Jefe de modelos (ejemplo)",estado:"Acordada"}));
  a.acuerdos=[{accion:"Reentrenar sin la variable de canal y confirmar Gini OOT",responsable:"Analista de modelos (ejemplo)",fecha:hoy(),estado:"Abierto"}];
  a.conformidad=a.conformidad.map(c=>({...c,nombre:c.area.includes("Negocio")?"Gerente de producto (ejemplo)":"Jefe de modelos (ejemplo)",estado:"Conforme",fecha:hoy(),medio:"Correo"}));
  a.estado="Aprobada";a.historial.push({fecha:new Date().toISOString(),version:1,cambio:"Aprobada",por:null});
  return a;
}

/* ---------------- editor */
let ED=null; // {a, dirty, base, ejemplo, tab}
function getPath(o,p){return p.split(".").reduce((x,k)=>x==null?x:x[k],o)}
function setPath(o,p,v){const ks=p.split(".");const last=ks.pop();const t=ks.reduce((x,k)=>x[k],o);t[last]=v}

async function openActa(aOrId,isEjemplo){
  await AStore.init();
  let a=typeof aOrId==="string"?AStore.docs.get(aOrId):aOrId;
  if(!a){$("#view").innerHTML=`<div class="doc"><h1>Acta no encontrada</h1><p>Puede que se haya eliminado o que aún no cargue. <a href="#actas">Volver a las actas</a>.</p></div>`;
    if(AStore.mode==="cargando"||AStore.docs.size===0){AStore.subs.clear();AStore.subs.add(()=>{if(AStore.docs.get(aOrId))openActa(aOrId)})}return}
  ED={a:JSON.parse(JSON.stringify(a)),dirty:false,base:a.actualizado,ejemplo:!!isEjemplo,tab:store.get("acta.tab","editar"),remote:false};
  AStore.subs.clear();
  AStore.subs.add(()=>{ if(!ED||ED.ejemplo||currentView!==ED.a.id)return;const r=AStore.docs.get(ED.a.id);
    if(!r){$("#a-remote").innerHTML=`<div class="a-banner warn">Esta acta fue eliminada por otra persona.</div>`;return}
    if(r.actualizado!==ED.base&&r.actualizado_por!==AStore.me){
      if(ED.dirty){ED.remote=true;$("#a-remote").innerHTML=`<div class="a-banner warn">Otra persona guardó cambios en esta acta. <button type="button" id="aLoadRemote">Cargar su versión</button> (perderás lo que no se guardó).</div>`;
        $("#aLoadRemote").onclick=()=>{ED.a=JSON.parse(JSON.stringify(r));ED.base=r.actualizado;ED.dirty=false;renderEditor()}}
      else{ED.a=JSON.parse(JSON.stringify(r));ED.base=r.actualizado;renderEditor(true)}}
  });
  renderEditor();
}
const ro=()=>ED.ejemplo||ED.a.estado==="Aprobada"||!AStore.canWrite;
function inp(path,o={}){const v=getPath(ED.a,path)??"";const id="f-"+path.replace(/\./g,"-");
  const dis=ro()?"disabled":"";
  if(o.area)return `<textarea id="${id}" data-p="${path}" rows="${o.rows||3}" ${dis} placeholder="${esc(o.ph||"")}" aria-label="${esc(o.label||path)}">${esc(v)}</textarea>`;
  if(o.sel)return `<select id="${id}" data-p="${path}" ${dis} aria-label="${esc(o.label||path)}">${o.sel.map(x=>`<option ${x===v?"selected":""}>${esc(x)}</option>`).join("")}</select>`;
  if(o.chk)return `<input type="checkbox" id="${id}" data-p="${path}" ${v?"checked":""} ${dis} aria-label="${esc(o.label||path)}">`;
  return `<input id="${id}" data-p="${path}" type="${o.type||"text"}" value="${esc(v)}" ${dis} ${o.list?`list="${o.list}"`:""} placeholder="${esc(o.ph||"")}" aria-label="${esc(o.label||path)}">`}
function rowsTable(key,cols,empty){
  const arr=ED.a[key];const dis=ro();
  return `<div class="tbl a-rows"><table><thead><tr>${cols.map(c=>`<th style="${c.w?`width:${c.w}`:""}">${c.h}</th>`).join("")}${dis?"":"<th class='x'><span class='sr'>Quitar</span></th>"}</tr></thead><tbody>
  ${arr.length?arr.map((r,i)=>`<tr>${cols.map(c=>`<td>${inp(`${key}.${i}.${c.k}`,{...c.o,label:`${c.h} ${i+1}`})}</td>`).join("")}${dis?"":`<td class="x"><button type="button" class="ico" data-del="${key}.${i}" aria-label="Quitar fila ${i+1}">✕</button></td>`}</tr>`).join("")
   :`<tr><td colspan="${cols.length+1}" class="a-none">${empty}</td></tr>`}</tbody></table></div>${dis?"":`<button type="button" class="add" data-add="${key}">+ Agregar</button>`}`}
function listEditor(key,ph){const arr=ED.a[key];const dis=ro();
  return `<ol class="a-ol">${arr.map((x,i)=>`<li>${inp(`${key}.${i}`,{ph,label:`${key} ${i+1}`})}${dis?"":`<button type="button" class="ico" data-del="${key}.${i}" aria-label="Quitar ${i+1}">✕</button>`}</li>`).join("")}</ol>${dis?"":`<button type="button" class="add" data-add="${key}">+ Agregar</button>`}`}

function renderEditor(keepFocus){
  const a=ED.a,t=TIPO[a.tipo]||{};const f=document.activeElement&&document.activeElement.id;
  const errs=validarActa(a);
  const reqOpts=`<datalist id="dl-req">${DATA.umbrales.map(u=>`<option value="${u.id}">${esc(u.tema)}</option>`).join("")}${DATA.requisitos.map(r=>`<option value="${r.id}">${esc(r.actividad.split("\n")[0].slice(0,80))}</option>`).join("")}</datalist>
    <datalist id="dl-umb">${DATA.umbrales.map(u=>`<option value="${u.id}">${esc(u.tema)}</option>`).join("")}</datalist>`;
  const flujo=ED.ejemplo?"":a.estado==="Borrador"?`<button type="button" class="primary" data-flujo="En revisión">Enviar a revisión</button>`:
    a.estado==="En revisión"?`<button type="button" class="primary" data-flujo="Aprobada">Aprobar acta</button><button type="button" data-flujo="Borrador">Devolver a borrador</button>`:
    `<button type="button" data-flujo="reabrir">Reabrir (nueva versión)</button>`;
  $("#view").innerHTML=`<div class="wide acta-ed">${reqOpts}
    <nav class="a-crumb"><a href="#actas">Actas de reunión</a> › <span class="mono">${esc(a.numero)}</span></nav>
    ${ED.ejemplo?`<div class="a-banner">Ejemplo con datos ficticios. No se guarda; puedes descargarlo para ver el formato.</div>`:""}
    <header class="a-head"><div><div class="a-kicker">${esc(t.acta||"Acta")} · ${esc(t.estandar||"")}</div><h1>${esc(t.nombre||a.tipo)}</h1>
      <div class="a-meta">${chipEstado(a.estado)} <span>Versión ${a.version}</span>${t.requisito?`<span>Requisito <a class="rid" href="#" data-id="${t.requisito}">${t.requisito}</a></span>`:""}<span id="a-save" class="a-save">${ED.ejemplo?"":AStore.canWrite?"Guardado":"Solo lectura"}</span></div></div>
      <div class="a-tools">${flujo}<button type="button" id="aDocx">Descargar Word</button><button type="button" id="aMd">Descargar Markdown</button><button type="button" id="aCopy">Copiar Markdown</button></div></header>
    <div id="a-remote"></div><div id="a-note" class="a-note" role="status"></div><div id="a-check"></div>
    <div class="a-tabs" role="tablist"><button role="tab" type="button" aria-selected="${ED.tab==="editar"}" data-tab="editar">Editar</button><button role="tab" type="button" aria-selected="${ED.tab==="doc"}" data-tab="doc">Vista de documento</button></div>
    ${ED.tab==="doc"?`<article class="a-paper">${renderMd(actaMd(a))}</article>`:`
    ${a.estado==="Aprobada"&&!ED.ejemplo?`<div class="a-banner ok">Acta aprobada (versión ${a.version}). Está bloqueada; para cambiarla, reábrela. La reapertura queda en el control de cambios.</div>`:""}
    <form class="a-form" id="aForm" onsubmit="return false">
      <section><h2>1. Datos generales</h2><div class="a-grid">
        <label class="ctl" for="f-numero"><span>N° de acta</span>${inp("numero",{label:"N° de acta"})}</label>
        <label class="ctl" for="f-modelo-codigo"><span>Código de modelo</span>${inp("modelo.codigo",{label:"Código de modelo"})}</label>
        <label class="ctl wide2" for="f-modelo-nombre"><span>Nombre del modelo</span>${inp("modelo.nombre",{label:"Nombre del modelo"})}</label>
        <label class="ctl" for="f-modelo-tier"><span>Tier</span>${inp("modelo.tier",{sel:["","I","II","III","IV"],label:"Tier"})}</label>
        <label class="ctl" for="f-modelo-tipo_modelo"><span>Tipo de modelo</span>${inp("modelo.tipo_modelo",{sel:["","lineal","ml","arbol","acp"],label:"Tipo de modelo"})}</label>
        <label class="ctl" for="f-fecha"><span>Fecha</span>${inp("fecha",{type:"date",label:"Fecha"})}</label>
        <label class="ctl" for="f-hora_inicio"><span>Inicio</span>${inp("hora_inicio",{type:"time",label:"Hora de inicio"})}</label>
        <label class="ctl" for="f-hora_fin"><span>Fin</span>${inp("hora_fin",{type:"time",label:"Hora de fin"})}</label>
        <label class="ctl" for="f-modalidad"><span>Modalidad</span>${inp("modalidad",{sel:MODALIDADES,label:"Modalidad"})}</label>
        <label class="ctl wide2" for="f-lugar"><span>Lugar o enlace</span>${inp("lugar",{label:"Lugar o enlace",ph:"Sala, o enlace de la reunión"})}</label>
        <label class="ctl wide2" for="f-secretario"><span>Secretario (redacta el acta)</span>${inp("secretario",{label:"Secretario"})}</label></div></section>
      <section><h2>2. Participantes</h2>${rowsTable("asistentes",[{k:"nombre",h:"Nombre",o:{ph:"Nombre y apellido"}},{k:"area",h:"Área"},{k:"rol",h:"Rol",w:"9rem",o:{sel:ROLES}},{k:"asistio",h:"Asistió",w:"4.5rem",o:{chk:true}}],"Agrega a los participantes.")}</section>
      <section><h2>3. Objetivo</h2>${inp("objetivo",{area:true,rows:2,label:"Objetivo"})}</section>
      <section><h2>4. Agenda</h2>${listEditor("agenda","Punto de agenda")}</section>
      <section><h2>5. Desarrollo de la reunión</h2><p class="a-help">Qué se presentó, qué se discutió y con qué datos. Separa párrafos con una línea en blanco.</p>${inp("resumen",{area:true,rows:7,label:"Desarrollo de la reunión",ph:"Ej.: Se presentaron tres modelos candidatos…"})}</section>
      <section><h2>6. Decisiones</h2><p class="a-help">Cada decisión enlaza al requisito o umbral del estándar que la exige.</p>${rowsTable("decisiones",[{k:"texto",h:"Decisión",o:{area:true,rows:2}},{k:"ref",h:"Requisito / umbral",w:"11rem",o:{list:"dl-req",ph:"DES-D4-06.03.01"}},{k:"responsable",h:"Responsable",w:"11rem"},{k:"estado",h:"Estado",w:"11rem",o:{sel:EST_DEC}}],"Sin decisiones.")}</section>
      <section><h2>7. Excepciones a umbrales</h2><p class="a-help">Solo si algún resultado no cumple un umbral (U-01 … U-17). Si va a Comité, márcalo.</p>${rowsTable("excepciones",[{k:"umbral",h:"Umbral",w:"7rem",o:{list:"dl-umb",ph:"U-11"}},{k:"valor",h:"Valor obtenido",w:"9rem"},{k:"justificacion",h:"Justificación",o:{area:true,rows:2}},{k:"comite",h:"Comité",w:"4.5rem",o:{chk:true}}],"No se registraron excepciones.")}</section>
      <section><h2>8. Acuerdos y pendientes</h2>${rowsTable("acuerdos",[{k:"accion",h:"Acción",o:{area:true,rows:2}},{k:"responsable",h:"Responsable",w:"11rem"},{k:"fecha",h:"Fecha compromiso",w:"10rem",o:{type:"date"}},{k:"estado",h:"Estado",w:"7rem",o:{sel:EST_ACU}}],"Sin pendientes.")}</section>
      <section><h2>9. Evidencias y entregables revisados</h2>${listEditor("evidencias","Ej.: PPT 9 · Indicadores del modelo final")}</section>
      <section><h2>10. Conformidad</h2><p class="a-help">La aprobación exige que todos estén en «Conforme». Registra el medio (correo, firma) como evidencia (VAL-M-01.03).</p>${rowsTable("conformidad",[{k:"nombre",h:"Nombre"},{k:"area",h:"Área / cargo"},{k:"estado",h:"Conformidad",w:"9rem",o:{sel:EST_CONF}},{k:"fecha",h:"Fecha",w:"10rem",o:{type:"date"}},{k:"medio",h:"Medio",w:"7rem",o:{sel:["Correo","Firma","En la reunión"]}}],"Agrega a quienes deben dar conformidad.")}</section>
      <section><h2>11. Control de cambios</h2><div class="tbl"><table><thead><tr><th>Versión</th><th>Fecha</th><th>Cambio</th><th>Por</th></tr></thead><tbody id="aHist">${a.historial.map(h=>`<tr><td>${h.version}</td><td class="mono">${esc(fmtFecha(h.fecha))}</td><td>${esc(h.cambio)}</td><td data-uid="${esc(h.por||"")}">—</td></tr>`).join("")}</tbody></table></div></section>
      ${ED.ejemplo||ro()?"":`<section class="a-danger"><button type="button" id="aDup">Duplicar acta</button><span id="aDelWrap"><button type="button" id="aDel" class="danger">Eliminar acta</button></span></section>`}
    </form>`}
  </div>`;
  // nombres del historial (solo ids guardados)
  AStore.names(a.historial.map(h=>h.por)).then(ps=>document.querySelectorAll("#aHist td[data-uid]").forEach(td=>{const p=ps[td.dataset.uid];if(p){td.textContent=p.isMe?"Tú":(p.name||"Integrante del equipo")}}));
  wireEditor();
  if(keepFocus&&f){const n=document.getElementById(f);if(n)n.focus()}
}
function nota(msg){const n=$("#a-note");if(n){n.textContent=msg;clearTimeout(nota.t);nota.t=setTimeout(()=>{n.textContent=""},6000)}}
function setSave(s){const n=$("#a-save");if(n)n.textContent=s}
let saveT=null;
function scheduleSave(){if(ED.ejemplo||ro())return;ED.dirty=true;setSave("Cambios sin guardar…");clearTimeout(saveT);saveT=setTimeout(doSave,1200)}
async function doSave(){
  if(!ED||ED.ejemplo)return;clearTimeout(saveT);setSave("Guardando…");
  try{await AStore.save(ED.a);ED.base=ED.a.actualizado;ED.dirty=false;ED.remote=false;$("#a-remote")&&($("#a-remote").innerHTML="");
    setSave(AStore.mode==="linea"?"Guardado en línea · "+new Date().toLocaleTimeString("es-PE",{timeStyle:"short"}):"Guardado en este navegador")}
  catch(e){setSave(e&&e.code==="invalid_argument"?"Solo lectura: tu acceso no permite guardar":e&&e.code==="quota_exceeded"?"Sin espacio para guardar":e&&e.code==="local_full"?"El navegador no tiene espacio":"No se pudo guardar; se reintentará con el próximo cambio");
    if(e&&e.code==="invalid_argument"){AStore.canWrite=false;renderEditor()}}
}
function wireEditor(){
  const v=$("#view");
  v.querySelectorAll("[data-tab]").forEach(b=>b.onclick=()=>{ED.tab=b.dataset.tab;store.set("acta.tab",ED.tab);renderEditor()});
  const form=$("#aForm");
  if(form){
    form.addEventListener("input",e=>{const p=e.target.dataset.p;if(!p)return;setPath(ED.a,p,e.target.type==="checkbox"?e.target.checked:e.target.value);scheduleSave()});
    form.addEventListener("change",e=>{const p=e.target.dataset.p;if(!p)return;setPath(ED.a,p,e.target.type==="checkbox"?e.target.checked:e.target.value);scheduleSave()});
    form.querySelectorAll("[data-add]").forEach(b=>b.onclick=()=>{const k=b.dataset.add;const blank={asistentes:{nombre:"",area:"",rol:"Informado",asistio:true},decisiones:{texto:"",ref:"",responsable:"",estado:"Pendiente de aprobación"},
      excepciones:{umbral:"",valor:"",justificacion:"",comite:false},acuerdos:{accion:"",responsable:"",fecha:"",estado:"Abierto"},conformidad:{nombre:"",area:"",estado:"Pendiente",fecha:"",medio:"Correo"}}[k];
      ED.a[k].push(blank?{...blank}:"");scheduleSave();renderEditor();const ins=document.querySelectorAll(`[data-p^="${k}.${ED.a[k].length-1}"]`);if(ins[0])ins[0].focus()});
    form.querySelectorAll("[data-del]").forEach(b=>b.onclick=()=>{const [k,i]=b.dataset.del.split(".");ED.a[k].splice(+i,1);scheduleSave();renderEditor()});
  }
  v.querySelectorAll("[data-flujo]").forEach(b=>b.onclick=async()=>{
    const to=b.dataset.flujo,a=ED.a,now=new Date().toISOString();
    if(to==="Aprobada"){const e=validarActa(a);if(e.length){$("#a-check").innerHTML=`<div class="a-banner warn"><b>Antes de aprobar:</b><ul>${e.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div>`;return}}
    $("#a-check").innerHTML="";
    if(to==="reabrir"){a.version+=1;a.estado="Borrador";a.historial.push({fecha:now,version:a.version,cambio:`Reapertura del acta (versión ${a.version})`,por:AStore.me})}
    else{a.historial.push({fecha:now,version:a.version,cambio:to==="En revisión"?"Enviada a revisión":to==="Aprobada"?"Aprobada":"Devuelta a borrador",por:AStore.me});a.estado=to}
    await doSave();renderEditor();nota(to==="Aprobada"?"Acta aprobada y bloqueada.":to==="reabrir"?`Acta reabierta como versión ${a.version}.`:"Estado actualizado: "+a.estado);
  });
  $("#aDocx").onclick=async()=>{nota("Preparando el documento Word…");try{const blob=await actaDocx(ED.a);await ofrecerArchivo(fileBase(ED.a)+".docx",blob,nota)}catch(e){nota("No se pudo generar el Word.")}};
  $("#aMd").onclick=()=>ofrecerArchivo(fileBase(ED.a)+".md",actaMd(ED.a),nota);
  $("#aCopy").onclick=()=>{const md=actaMd(ED.a);const fb=()=>{$("#a-check").innerHTML=`<textarea class="copybox" id="aCopyBox" aria-label="Acta en Markdown"></textarea>`;const t=$("#aCopyBox");t.value=md;t.select();nota("Texto seleccionado: cópialo con Ctrl+C.")};
    try{navigator.clipboard.writeText(md).then(()=>nota("Acta copiada en Markdown."),fb)}catch(e){fb()}};
  $("#aDup")&&($("#aDup").onclick=async()=>{const src=ED.a;const n=AStore.list().filter(x=>x.modelo.codigo===src.modelo.codigo).length+1;
    const c=actaNueva(TIPO[src.tipo]||TIPO.LIBRE,{...src.modelo,fecha:hoy()},n);
    Object.assign(c,{objetivo:src.objetivo,agenda:[...src.agenda],asistentes:src.asistentes.map(x=>({...x})),evidencias:[...src.evidencias]});
    c.historial[0].cambio=`Creación a partir de ${src.numero}`;await AStore.save(c);location.hash="#"+c.id});
  $("#aDel")&&($("#aDel").onclick=()=>{$("#aDelWrap").innerHTML=`<span class="a-confirm">¿Eliminar ${esc(ED.a.numero)} para todo el equipo? <button type="button" class="danger" id="aDelOk">Sí, eliminar</button><button type="button" id="aDelNo">Cancelar</button></span>`;
    $("#aDelNo").onclick=()=>renderEditor();$("#aDelOk").onclick=async()=>{await AStore.remove(ED.a.id);ED=null;location.hash="#actas"}});
}
window.addEventListener("beforeunload",e=>{if(ED&&ED.dirty){doSave()}});
