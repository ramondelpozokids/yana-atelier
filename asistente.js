(function () {
  const LOGO = 'logo-asistente.webp';
  const WA = 'https://wa.me/34638753937';

  const QUICK = [
    'Servicios',
    'Tarifas',
    'Productos',
    'Clases',
    'Ubicación',
    'Reservar cita'
  ];

  const FAQS = [
    {
      keys: ['hola', 'buenas', 'hey', 'saludo'],
      answer: 'Hola. Soy el asistente de Yana Yavorskaya Atelier. Puedo contarte sobre servicios, tarifas, clases, productos a la venta, horario y cómo reservar cita.'
    },
    {
      keys: ['servicio', 'qué hacéis', 'que haceis', 'que ofrece', 'intervencion', 'intervención'],
      answer: 'El atelier ofrece tres intervenciones:\n• Alta costura: diseño y confección desde cero.\n• Ajuste de precisión: corrección técnica de prendas.\n• Transformación: rediseño de piezas con valor sentimental.\nTambién hay clases de costura y una selección privada de prendas y calzado a la venta.'
    },
    {
      keys: ['alta costura', 'a medida', 'confeccion', 'confección', 'diseño'],
      answer: 'Alta costura: diseño y confección desde cero con patrón propio, tejidos seleccionados y acabados artesanales. Precio orientativo desde 350 €. Incluye 3 pruebas de ajuste. Entrega habitual: 3-4 semanas. Cada proyecto se presupuesta en cita.'
    },
    {
      keys: ['ajuste', 'bajo', 'cremallera', 'arreglar', 'arreglo', 'cintura'],
      answer: 'Ajuste básico: desde 35 €/prenda. Incluye bajos, ajuste de cintura, cambio de cremalleras y reparaciones simples. Entrega en 3-5 días. El ajuste de precisión corrige la prenda a tu silueta con trabajo técnico de atelier.'
    },
    {
      keys: ['transform', 'rediseño', 'redisen', 'nueva vida', 'antes', 'despues', 'después'],
      answer: 'En Trabajos del atelier hay casos reales: vestido floral recuperado, vestido de gala con acabado de sastrería y ajuste de chaqueta. No son tutoriales para casa: se valora la prenda en cita. Transformación desde 120 €. Ajuste básico desde 35 €.'
    },
    {
      keys: ['tarifa', 'precio', 'cuesta', 'cuanto', 'cuánto', 'presupuesto'],
      answer: 'Tarifas orientativas de servicios:\n• Ajuste básico: 35 €/prenda\n• Transformación: desde 120 €\n• Alta costura: desde 350 €\nClases: 40 €/hora individual o 65 €/mes en grupo.\nLa selección de productos tiene precios propios (20-45 €). Cada encargo de atelier se confirma en cita.'
    },
    {
      keys: ['clase', 'aprender', 'curso', 'alumna', 'coser'],
      answer: 'Clases de costura en el propio atelier, todos los niveles.\n• Individual: 40 €/hora, horario a convenir. Primera clase de valoración gratuita.\n• Grupo: 65 €/mes, máx. 5 alumnas, 1 sesión semanal de 2 horas. Máquina y material básico incluidos. Sin permanencia.'
    },
    {
      keys: ['producto', 'ropa', 'falda', 'blusa', 'zapato', 'calzado', 'venta', 'wallapop', 'comprar', 'lote'],
      answer: 'Hay una selección privada en Productos:\nPrendas 20-25 € (blusa camuflaje, faldas tejano, azul, espiga, floral, patchwork, encaje menta).\nCalzado talla 37: tacón azul 25 €, botines oxford 30 €, charol Zinda 45 €.\nLotes: 2 faldas 35 € · 3 pares 85 € · lote completo a convenir.\nPrecios negociables. Envío o entrega en Madrid.'
    },
    {
      keys: ['horario', 'hora', 'abierto', 'cuando', 'cuándo'],
      answer: 'Horario:\nLunes a viernes 10:00-19:00\nSábados 10:00-14:00\nDomingos y festivos cerrado.\nLa atención es exclusivamente con cita previa.'
    },
    {
      keys: ['ubicacion', 'ubicación', 'direccion', 'dirección', 'donde', 'dónde', 'metro', 'madrid', 'vallecas', 'mapa'],
      answer: 'Yana Yavorskaya Atelier\nCalle González Soto, 40, planta 1B\n28038 Madrid\nMetro: Nueva Numancia / Puente de Vallecas (L1).\nTeléfono 638 753 937 · yana140764@gmail.com'
    },
    {
      keys: ['cita', 'reservar', 'contacto', 'formulario', 'whatsapp', 'telefono', 'teléfono', 'email', 'correo'],
      answer: 'Para reservar: formulario de contacto en la web, WhatsApp o llamada al 638 753 937, o email yana140764@gmail.com. Respuesta habitual en menos de 24 horas. Toda la atención es con cita previa.'
    },
    {
      keys: ['yana', 'sobre', 'quien', 'quién', 'atelier', 'juliette'],
      answer: 'Yana Yavorskaya es la mano detrás del atelier: análisis técnico, patronaje y acabado personal. Formada en sastrería y confección tradicionales, trabajó en Juliette Atelier. Hoy combina esa precisión con un trato cercano y sin prisas.'
    },
    {
      keys: ['proceso', 'diagnostico', 'diagnóstico', 'como trabaja', 'cómo trabaja'],
      answer: 'Proceso artesanal en tres pasos:\n1. Diagnóstico: tejido, caída y estructura.\n2. Intervención: ajuste, forma y volumen a mano.\n3. Acabado final: refinamiento y control de calidad.'
    },
    {
      keys: ['envio', 'envío', 'entrega', 'negociable'],
      answer: 'En productos: envío o entrega en mano en Madrid. Medidas exactas bajo petición. Los precios de ficha son negociables.'
    },
    {
      keys: ['gracias', 'ok', 'vale'],
      answer: 'Encantada de ayudar. Si quieres hablar con Yana, usa WhatsApp (abajo a la izquierda) o el formulario de contacto.'
    }
  ];

  function reply(text) {
    const m = (text || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    for (const item of FAQS) {
      if (item.keys.some((k) => m.includes(k.normalize('NFD').replace(/[\u0300-\u036f]/g, '')))) {
        return item.answer;
      }
    }
    return 'Puedo ayudarte con servicios, tarifas, clases, productos, horario o ubicación. Escribe, por ejemplo: «alta costura», «clases» o «productos». Para una consulta personal, WhatsApp 638 753 937.';
  }

  function addMsg(log, who, text) {
    const el = document.createElement('div');
    el.className = 'chat-msg ' + who;
    el.textContent = text;
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
  }

  function ask(log, text) {
    const q = (text || '').trim();
    if (!q) return;
    addMsg(log, 'user', q);
    addMsg(log, 'bot', reply(q));
  }

  document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('chatPanel')) return;

    const fab = document.createElement('button');
    fab.className = 'chat-fab';
    fab.type = 'button';
    fab.setAttribute('aria-label', 'Abrir asistente de Yana');
    fab.innerHTML = '<img src="' + LOGO + '" alt="Logo Yana Yavorskaya">';

    const panel = document.createElement('div');
    panel.className = 'chat-panel';
    panel.id = 'chatPanel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Asistente del atelier');
    panel.innerHTML =
      '<div class="chat-head">' +
        '<img src="' + LOGO + '" alt="">' +
        '<div><strong>Yana Yavorskaya</strong><span>Asistente del atelier</span></div>' +
        '<button type="button" aria-label="Cerrar chat">&times;</button>' +
      '</div>' +
      '<div class="chat-log" id="chatLog"></div>' +
      '<div class="chat-quick" id="chatQuick"></div>' +
      '<form class="chat-form" id="chatForm">' +
        '<input type="text" id="chatInput" placeholder="Escribe tu pregunta..." autocomplete="off">' +
        '<button type="submit">Enviar</button>' +
      '</form>';

    document.body.appendChild(panel);
    document.body.appendChild(fab);

    const log = panel.querySelector('#chatLog');
    const quick = panel.querySelector('#chatQuick');
    const form = panel.querySelector('#chatForm');
    const input = panel.querySelector('#chatInput');
    const closeBtn = panel.querySelector('.chat-head button');

    addMsg(log, 'bot', 'Hola. Pregúntame por servicios, tarifas, clases, productos o cómo reservar cita. Si prefieres hablar con Yana, el botón de WhatsApp está abajo a la izquierda.');

    QUICK.forEach(function (label) {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = label;
      b.addEventListener('click', function () { ask(log, label); });
      quick.appendChild(b);
    });

    function toggle() {
      const open = panel.classList.toggle('open');
      fab.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) input.focus();
    }

    fab.addEventListener('click', toggle);
    closeBtn.addEventListener('click', function () {
      panel.classList.remove('open');
      fab.setAttribute('aria-expanded', 'false');
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      ask(log, input.value);
      input.value = '';
    });
  });
})();
