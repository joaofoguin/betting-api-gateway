const GATEWAY = "http://127.0.0.1:8000";

// --- SISTEMA DE ACESSO (JWT) ---

async function executarLogin() {
    const usuario = document.getElementById('user').value;
    const senha = document.getElementById('pass').value;

    try {
        const res = await fetch(`${GATEWAY}/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ usuario, senha })
        });

        if (res.ok) {
            const dados = await res.json();
            localStorage.setItem('token_sd', dados.token);
            verificarStatusLogin();
        } else {
            alert("Credenciais Inválidas");
        }
    } catch (err) {
        alert("Erro ao conectar com o Integrador");
    }
}

function verificarStatusLogin() {
    const token = localStorage.getItem('token_sd');
    if (token) {
        document.getElementById('telaLogin').style.display = 'none';
        document.getElementById('telaPrincipal').style.display = 'block';
        atualizarPainel();
    } else {
        document.getElementById('telaLogin').style.display = 'flex';
        document.getElementById('telaPrincipal').style.display = 'none';
    }
}

function logout() {
    localStorage.removeItem('token_sd');
    verificarStatusLogin();
}

// --- FUNÇÃO AUXILIAR PARA REQUISIÇÕES AUTENTICADAS ---

async function fetchProtegido(url, options = {}) {
    const token = localStorage.getItem('token_sd');
    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`
    };
    return fetch(url, { ...options, headers });
}

// --- LOGICA DE LUTADORES (API EXTERNA) ---

async function carregarLutadores() {
    const res = await fetchProtegido(`${GATEWAY}/lutadores`);
    const lutadores = await res.json();
    
    // Atualiza Selects
    const htmlOptions = lutadores.map(l => `<option value="${l.id}">${l.nome}</option>`).join('');
    document.getElementById('selLutador1').innerHTML = htmlOptions;
    document.getElementById('selLutador2').innerHTML = htmlOptions;

    // Atualiza Lista
    document.getElementById('listaLutadores').innerHTML = lutadores.map(l => `
        <div class="item">
            <div><b>${l.nome}</b><br><small>${l.categoria}</small></div>
            <button class="btn-del" onclick="deletarLutador(${l.id})">🗑️</button>
        </div>
    `).join('');
}

async function cadastrarLutador() {
    const payload = {
        nome: document.getElementById('nomeLutador').value,
        apelido: document.getElementById('apelidoLutador').value,
        categoria: document.getElementById('catLutador').value,
        arte: document.getElementById('arteLutador').value
    };

    await fetchProtegido(`${GATEWAY}/lutadores`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    });
    carregarLutadores();
}

async function deletarLutador(id) {
    await fetchProtegido(`${GATEWAY}/lutadores/${id}`, { method: 'DELETE' });
    carregarLutadores();
}

// --- LOGICA DE LUTAS (SUA API - RSA) ---

async function listarLutas() {
    const res = await fetchProtegido(`${GATEWAY}/lutas`);
    const lutas = await res.json();
    document.getElementById('listaLutas').innerHTML = lutas.map(l => `
        <div class="item">
            <div>📅 ${l.data} | ${l.nome_lutador1} ⚔️ ${l.nome_lutador2}</div>
            <button class="btn-del" onclick="deletarLuta(${l.id})">❌</button>
        </div>
    `).join('');
}

async function agendarLuta() {
    const s1 = document.getElementById('selLutador1');
    const s2 = document.getElementById('selLutador2');
    
    const payload = {
        data: document.getElementById('dataLuta').value,
        horario: document.getElementById('horaLuta').value,
        id_lutador1: parseInt(s1.value),
        id_lutador2: parseInt(s2.value),
        nome_lutador1: s1.options[s1.selectedIndex].text,
        nome_lutador2: s2.options[s2.selectedIndex].text
    };

    await fetchProtegido(`${GATEWAY}/lutas`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    });
    listarLutas();
}

async function deletarLuta(id) {
    await fetchProtegido(`${GATEWAY}/lutas/${id}`, { method: 'DELETE' });
    listarLutas();
}

function atualizarPainel() {
    carregarLutadores();
    listarLutas();
}

window.onload = verificarStatusLogin;