import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import { Calculator, TrendingUp, Users, Search, Menu, X, DollarSign, Target, Zap } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Sales Calculator Component
const SalesCalculator = () => {
  const [formData, setFormData] = useState({
    produto: '',
    preco_custo: '',
    impostos: '',
    frete: '',
    margem_desejada: '20'
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const calculateSales = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(`${API}/calcular-vendas`, {
        produto: formData.produto,
        preco_custo: parseFloat(formData.preco_custo),
        impostos: parseFloat(formData.impostos) || 0,
        frete: parseFloat(formData.frete) || 0,
        margem_desejada: parseFloat(formData.margem_desejada)
      });
      setResult(response.data);
      loadHistory();
    } catch (error) {
      console.error('Erro no cálculo:', error);
      alert('Erro ao calcular. Verifique os dados inseridos.');
    }
    setLoading(false);
  };

  const loadHistory = async () => {
    try {
      const response = await axios.get(`${API}/historico-calculos`);
      setHistory(response.data.slice(0, 5));
    } catch (error) {
      console.error('Erro ao carregar histórico:', error);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div className="calculator-container">
      <div className="calculator-header">
        <Calculator className="header-icon" />
        <h2>Calculadora de Vendas</h2>
        <p>Calcule o preço ideal e sua margem de lucro</p>
      </div>

      <form onSubmit={calculateSales} className="calculator-form">
        <div className="form-group">
          <label>Nome do Produto</label>
          <input
            type="text"
            name="produto"
            value={formData.produto}
            onChange={handleInputChange}
            placeholder="Ex: Fone Bluetooth"
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Preço de Custo (R$)</label>
            <input
              type="number"
              step="0.01"
              name="preco_custo"
              value={formData.preco_custo}
              onChange={handleInputChange}
              placeholder="50.00"
              required
            />
          </div>
          <div className="form-group">
            <label>Impostos (R$)</label>
            <input
              type="number"
              step="0.01"
              name="impostos"
              value={formData.impostos}
              onChange={handleInputChange}
              placeholder="5.00"
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Frete (R$)</label>
            <input
              type="number"
              step="0.01"
              name="frete"
              value={formData.frete}
              onChange={handleInputChange}
              placeholder="10.00"
            />
          </div>
          <div className="form-group">
            <label>Margem Desejada (%)</label>
            <input
              type="number"
              name="margem_desejada"
              value={formData.margem_desejada}
              onChange={handleInputChange}
              placeholder="20"
              required
            />
          </div>
        </div>

        <button type="submit" disabled={loading} className="calculate-btn">
          {loading ? 'Calculando...' : 'Calcular Preço de Venda'}
        </button>
      </form>

      {result && (
        <div className="result-container">
          <h3>Resultado do Cálculo</h3>
          <div className="result-grid">
            <div className="result-item">
              <span className="result-label">Preço de Venda:</span>
              <span className="result-value price">R$ {result.preco_venda.toFixed(2)}</span>
            </div>
            <div className="result-item">
              <span className="result-label">Lucro Bruto:</span>
              <span className="result-value profit">R$ {result.lucro_bruto.toFixed(2)}</span>
            </div>
            <div className="result-item">
              <span className="result-label">Lucro Líquido:</span>
              <span className="result-value profit">R$ {result.lucro_liquido.toFixed(2)}</span>
            </div>
          </div>
        </div>
      )}

      {history.length > 0 && (
        <div className="history-container">
          <h4>Últimos Cálculos</h4>
          <div className="history-list">
            {history.map((item) => (
              <div key={item.id} className="history-item">
                <span className="history-product">{item.produto}</span>
                <span className="history-price">R$ {item.preco_venda.toFixed(2)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Niche Finder Component
const NicheFinder = () => {
  const [niches, setNiches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    loadNiches();
  }, []);

  const loadNiches = async () => {
    try {
      const response = await axios.get(`${API}/nichos`);
      setNiches(response.data);
    } catch (error) {
      console.error('Erro ao carregar nichos:', error);
    }
    setLoading(false);
  };

  const filteredNiches = niches.filter(niche =>
    niche.nome.toLowerCase().includes(filter.toLowerCase()) ||
    niche.categoria.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="feature-container">
      <div className="feature-header">
        <Target className="header-icon" />
        <h2>Busca de Nichos</h2>
        <p>Encontre nichos lucrativos para seu negócio</p>
      </div>

      <div className="search-container">
        <input
          type="text"
          placeholder="Buscar por nicho ou categoria..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="search-input"
        />
      </div>

      {loading ? (
        <div className="loading">Carregando nichos...</div>
      ) : (
        <div className="niches-grid">
          {filteredNiches.map((niche) => (
            <div key={niche.id} className="niche-card">
              <div className="niche-header">
                <h3>{niche.nome}</h3>
                <span className="niche-category">{niche.categoria}</span>
              </div>
              <p className="niche-description">{niche.descricao}</p>
              <div className="niche-metrics">
                <div className="metric">
                  <span className="metric-label">Demanda:</span>
                  <span className={`metric-value ${niche.demanda.toLowerCase()}`}>{niche.demanda}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Competição:</span>
                  <span className={`metric-value ${niche.competicao.toLowerCase()}`}>{niche.competicao}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Rentabilidade:</span>
                  <span className={`metric-value ${niche.rentabilidade.toLowerCase()}`}>{niche.rentabilidade}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// Supplier Finder Component
const SupplierFinder = () => {
  const [suppliers, setSuppliers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    loadSuppliers();
  }, []);

  const loadSuppliers = async () => {
    try {
      const response = await axios.get(`${API}/fornecedores`);
      setSuppliers(response.data);
    } catch (error) {
      console.error('Erro ao carregar fornecedores:', error);
    }
    setLoading(false);
  };

  const filteredSuppliers = suppliers.filter(supplier =>
    supplier.nome.toLowerCase().includes(filter.toLowerCase()) ||
    supplier.categoria.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="feature-container">
      <div className="feature-header">
        <Users className="header-icon" />
        <h2>Encontrar Fornecedores</h2>
        <p>Conecte-se com fornecedores confiáveis</p>
      </div>

      <div className="search-container">
        <input
          type="text"
          placeholder="Buscar fornecedores por nome ou categoria..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="search-input"
        />
      </div>

      {loading ? (
        <div className="loading">Carregando fornecedores...</div>
      ) : (
        <div className="suppliers-grid">
          {filteredSuppliers.map((supplier) => (
            <div key={supplier.id} className="supplier-card">
              <div className="supplier-header">
                <h3>{supplier.nome}</h3>
                <div className="supplier-rating">
                  ⭐ {supplier.avaliacao}
                </div>
              </div>
              <div className="supplier-info">
                <span className="supplier-category">{supplier.categoria}</span>
                <span className="supplier-location">📍 {supplier.localizacao}</span>
              </div>
              <div className="supplier-products">
                <h4>Produtos Principais:</h4>
                <div className="products-list">
                  {supplier.produtos_principais.map((produto, index) => (
                    <span key={index} className="product-tag">{produto}</span>
                  ))}
                </div>
              </div>
              <div className="supplier-contact">
                <span className="contact-info">📧 {supplier.contato}</span>
                <span className="min-order">Pedido mín: {supplier.preco_minimo}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// Trend Analysis Component
const TrendAnalysis = () => {
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTrends();
  }, []);

  const loadTrends = async () => {
    try {
      const response = await axios.get(`${API}/tendencias`);
      setTrends(response.data);
    } catch (error) {
      console.error('Erro ao carregar tendências:', error);
    }
    setLoading(false);
  };

  return (
    <div className="feature-container">
      <div className="feature-header">
        <TrendingUp className="header-icon" />
        <h2>Análise de Tendências</h2>
        <p>Descubra produtos em alta no mercado</p>
      </div>

      {loading ? (
        <div className="loading">Carregando tendências...</div>
      ) : (
        <div className="trends-grid">
          {trends.map((trend) => (
            <div key={trend.id} className="trend-card">
              <div className="trend-header">
                <h3>{trend.produto}</h3>
                <span className="trend-category">{trend.categoria}</span>
              </div>
              <div className="trend-metrics">
                <div className="trend-metric">
                  <span className="metric-icon">📈</span>
                  <div>
                    <span className="metric-label">Crescimento</span>
                    <span className="metric-value growth">{trend.crescimento}</span>
                  </div>
                </div>
                <div className="trend-metric">
                  <span className="metric-icon">🔍</span>
                  <div>
                    <span className="metric-label">Volume de Busca</span>
                    <span className="metric-value">{trend.volume_busca}</span>
                  </div>
                </div>
                <div className="trend-metric">
                  <span className="metric-icon">📅</span>
                  <div>
                    <span className="metric-label">Sazonalidade</span>
                    <span className="metric-value">{trend.sazonalidade}</span>
                  </div>
                </div>
                <div className="trend-metric">
                  <span className="metric-icon">💡</span>
                  <div>
                    <span className="metric-label">Oportunidade</span>
                    <span className={`metric-value ${trend.oportunidade.toLowerCase().replace(' ', '-')}`}>
                      {trend.oportunidade}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// Main App Component
function App() {
  const [activeTab, setActiveTab] = useState('calculator');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const tabs = [
    { id: 'calculator', name: 'Calculadora', icon: Calculator },
    { id: 'niches', name: 'Nichos', icon: Target },
    { id: 'suppliers', name: 'Fornecedores', icon: Users },
    { id: 'trends', name: 'Tendências', icon: TrendingUp }
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'calculator':
        return <SalesCalculator />;
      case 'niches':
        return <NicheFinder />;
      case 'suppliers':
        return <SupplierFinder />;
      case 'trends':
        return <TrendAnalysis />;
      default:
        return <SalesCalculator />;
    }
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <div className="header-container">
          <div className="logo">
            <DollarSign className="logo-icon" />
            <h1>OtimizaVenda</h1>
          </div>
          
          {/* Desktop Navigation */}
          <nav className="desktop-nav">
            {tabs.map((tab) => {
              const IconComponent = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`nav-item ${activeTab === tab.id ? 'active' : ''}`}
                >
                  <IconComponent size={20} />
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </nav>

          {/* Mobile Menu Button */}
          <button 
            className="mobile-menu-btn"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <nav className="mobile-nav">
            {tabs.map((tab) => {
              const IconComponent = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id);
                    setMobileMenuOpen(false);
                  }}
                  className={`mobile-nav-item ${activeTab === tab.id ? 'active' : ''}`}
                >
                  <IconComponent size={20} />
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </nav>
        )}
      </header>

      {/* Main Content */}
      <main className="main-content">
        {renderContent()}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-container">
          <div className="footer-section">
            <h3>OtimizaVenda</h3>
            <p>Sua plataforma completa para otimização de vendas online</p>
          </div>
          <div className="footer-section">
            <h4>Ferramentas</h4>
            <ul>
              <li>Calculadora de Vendas</li>
              <li>Busca de Nichos</li>
              <li>Encontrar Fornecedores</li>
              <li>Análise de Tendências</li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Suporte</h4>
            <ul>
              <li>Como usar</li>
              <li>FAQ</li>
              <li>Contato</li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2025 OtimizaVenda. Todos os direitos reservados.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;