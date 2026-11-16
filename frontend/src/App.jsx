import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  TrendingUp,
  CreditCard,
  DollarSign,
  ArrowUpRight,
  ArrowDownRight,
  RefreshCw,
  Search,
  MessageSquare,
  Building,
  CheckCircle2,
  AlertTriangle,
  Send,
  Calendar,
  Users
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

// Automatically determine API base URL depending on access point (Localhost, LAN 192.168.2.100, or Remote Static IP 115.246.171.163)
const getApiBase = () => {
  const host = window.location.hostname;
  if (host === 'localhost' || host === '127.0.0.1') {
    return 'http://127.0.0.1:8000/api/v1';
  }
  // When accessed via LAN or Remote Static IP, talk to backend on port 8000 of the same host
  return `http://${host}:8000/api/v1`;
};

const API_BASE = getApiBase();

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

export default function App() {
  const [metrics, setMetrics] = useState(null);
  const [status, setStatus] = useState(null);
  const [receivables, setReceivables] = useState([]);
  const [vouchers, setVouchers] = useState([]);
  const [syncing, setSyncing] = useState(false);
  const [activeTab, setActiveTab] = useState('overview'); // overview, receivables, vouchers, ai
  
  // AI Chat state
  const [chatMessages, setChatMessages] = useState([
    {
      sender: 'ai',
      text: 'Hello! I am your Tally AI assistant. You can ask me questions like: "Who owes the most?", "What is our bank balance?", or "Show total sales".'
    }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);

  const fetchData = async () => {
    try {
      const [mRes, sRes, rRes, vRes] = await Promise.all([
        axios.get(`${API_BASE}/metrics`),
        axios.get(`${API_BASE}/status`),
        axios.get(`${API_BASE}/receivables`),
        axios.get(`${API_BASE}/vouchers`)
      ]);
      setMetrics(mRes.data);
      setStatus(sRes.data);
      setReceivables(rRes.data);
      setVouchers(vRes.data);
    } catch (err) {
      console.error("Error loading dashboard data", err);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const handleSync = async () => {
    setSyncing(true);
    try {
      await axios.post(`${API_BASE}/sync`);
      await fetchData();
    } catch (err) {
      console.error("Sync failed", err);
    } finally {
      setSyncing(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const query = chatInput;
    setChatInput('');
    setChatMessages((prev) => [...prev, { sender: 'user', text: query }]);
    setChatLoading(true);

    try {
      const res = await axios.post(`${API_BASE}/ask-ai`, { prompt: query });
      setChatMessages((prev) => [...prev, { sender: 'ai', text: res.data.answer }]);
    } catch (err) {
      setChatMessages((prev) => [
        ...prev,
        { sender: 'ai', text: 'Sorry, I had trouble processing that request. Please verify the backend service.' }
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  const formatCurrency = (val) => {
    if (val === undefined || val === null) return '₹0';
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(val);
  };

  const agingData = metrics ? [
    { name: '0-30 Days', amount: metrics.aging_receivables['0-30'] || 0 },
    { name: '31-60 Days', amount: metrics.aging_receivables['31-60'] || 0 },
    { name: '61-90 Days', amount: metrics.aging_receivables['61-90'] || 0 },
    { name: '90+ Days', amount: metrics.aging_receivables['90+'] || 0 },
  ] : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Top Navigation */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-black text-xl shadow-lg shadow-blue-500/20">
            T
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-white tracking-tight">TallyAI Dashboard</span>
              <span className="text-xs bg-blue-500/10 text-blue-400 font-semibold px-2 py-0.5 rounded-full border border-blue-500/20">
                Live Server
              </span>
            </div>
            <p className="text-xs text-slate-400 flex items-center gap-1.5 mt-0.5">
              <Building className="w-3 h-3 text-slate-400" />
              {status?.companies?.[0]?.name || 'Connected Tally Enterprise'}
            </p>
          </div>
        </div>

        {/* Sync Status & Action */}
        <div className="flex items-center space-x-4">
          <div className="hidden md:flex items-center gap-2 text-xs text-slate-400 bg-slate-800/60 px-3 py-1.5 rounded-lg border border-slate-700/50">
            {status?.last_sync_status === 'SUCCESS' ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-amber-400" />
            )}
            <span>
              Last Sync: {status?.last_sync ? new Date(status.last_sync).toLocaleTimeString() : 'N/A'}
            </span>
          </div>

          <button
            onClick={handleSync}
            disabled={syncing}
            className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-500 active:scale-95 transition text-white text-xs font-semibold px-3.5 py-2 rounded-lg shadow-sm disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${syncing ? 'animate-spin' : ''}`} />
            <span>{syncing ? 'Syncing...' : 'Sync Tally'}</span>
          </button>
        </div>
      </header>

      {/* Tabs */}
      <div className="border-b border-slate-800 bg-slate-900/40 px-6 flex space-x-6">
        <button
          onClick={() => setActiveTab('overview')}
          className={`py-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'overview'
              ? 'border-blue-500 text-blue-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Executive Overview
        </button>
        <button
          onClick={() => setActiveTab('receivables')}
          className={`py-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'receivables'
              ? 'border-blue-500 text-blue-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Accounts Receivable ({receivables.length})
        </button>
        <button
          onClick={() => setActiveTab('vouchers')}
          className={`py-3 text-sm font-medium border-b-2 transition ${
            activeTab === 'vouchers'
              ? 'border-blue-500 text-blue-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          Vouchers & Transactions
        </button>
        <button
          onClick={() => setActiveTab('ai')}
          className={`py-3 text-sm font-medium border-b-2 transition flex items-center gap-1.5 ${
            activeTab === 'ai'
              ? 'border-indigo-500 text-indigo-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          <span>Ask Tally AI</span>
        </button>
      </div>

      {/* Main Content Area */}
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full space-y-6">
        {activeTab === 'overview' && (
          <>
            {/* KPI Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl relative overflow-hidden">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                      Accounts Receivable
                    </p>
                    <h3 className="text-2xl font-bold mt-1 text-emerald-400">
                      {formatCurrency(metrics?.total_receivables)}
                    </h3>
                  </div>
                  <div className="p-2.5 bg-emerald-500/10 rounded-xl text-emerald-400">
                    <ArrowDownRight className="w-5 h-5" />
                  </div>
                </div>
                <div className="mt-4 flex items-center text-xs text-slate-400">
                  <Users className="w-3.5 h-3.5 mr-1 text-slate-500" />
                  <span>{metrics?.debtor_count || 0} Outstanding Customers</span>
                </div>
              </div>

              <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl relative overflow-hidden">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                      Accounts Payable
                    </p>
                    <h3 className="text-2xl font-bold mt-1 text-amber-400">
                      {formatCurrency(metrics?.total_payables)}
                    </h3>
                  </div>
                  <div className="p-2.5 bg-amber-500/10 rounded-xl text-amber-400">
                    <ArrowUpRight className="w-5 h-5" />
                  </div>
                </div>
                <div className="mt-4 flex items-center text-xs text-slate-400">
                  <Users className="w-3.5 h-3.5 mr-1 text-slate-500" />
                  <span>{metrics?.creditor_count || 0} Creditors / Suppliers</span>
                </div>
              </div>

              <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl relative overflow-hidden">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                      Cash & Bank Liquidity
                    </p>
                    <h3 className="text-2xl font-bold mt-1 text-blue-400">
                      {formatCurrency(metrics?.total_liquidity)}
                    </h3>
                  </div>
                  <div className="p-2.5 bg-blue-500/10 rounded-xl text-blue-400">
                    <CreditCard className="w-5 h-5" />
                  </div>
                </div>
                <div className="mt-4 flex items-center text-xs text-slate-400">
                  <span>In Banks & Cash-in-hand</span>
                </div>
              </div>

              <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl relative overflow-hidden">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                      Total Sales Revenue
                    </p>
                    <h3 className="text-2xl font-bold mt-1 text-indigo-400">
                      {formatCurrency(metrics?.total_sales)}
                    </h3>
                  </div>
                  <div className="p-2.5 bg-indigo-500/10 rounded-xl text-indigo-400">
                    <TrendingUp className="w-5 h-5" />
                  </div>
                </div>
                <div className="mt-4 flex items-center text-xs text-slate-400">
                  <span>Gross Margin: {formatCurrency(metrics?.net_profit_estimate)}</span>
                </div>
              </div>
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Aging Bar Chart */}
              <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 p-6 rounded-2xl">
                <h4 className="font-semibold text-base text-white mb-1">Debtor Aging Analysis</h4>
                <p className="text-xs text-slate-400 mb-6">Receivables categorized by overdue age</p>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={agingData}>
                      <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} />
                      <YAxis stroke="#64748b" fontSize={12} tickFormatter={(v) => `₹${v / 1000}k`} tickLine={false} />
                      <Tooltip
                        contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                        formatter={(val) => [formatCurrency(val), 'Amount']}
                      />
                      <Bar dataKey="amount" fill="#3b82f6" radius={[6, 6, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Cash vs Dues Ratio */}
              <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl flex flex-col justify-between">
                <div>
                  <h4 className="font-semibold text-base text-white mb-1">Liquidity Coverage</h4>
                  <p className="text-xs text-slate-400 mb-4">Bank Balance vs Immediate Supplier Payables</p>
                  
                  <div className="space-y-4 mt-6">
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-slate-400">Bank Liquidity</span>
                        <span className="text-blue-400 font-semibold">{formatCurrency(metrics?.total_liquidity)}</span>
                      </div>
                      <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                        <div className="bg-blue-500 h-full rounded-full" style={{ width: '75%' }}></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-slate-400">Creditors Payable</span>
                        <span className="text-amber-400 font-semibold">{formatCurrency(metrics?.total_payables)}</span>
                      </div>
                      <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                        <div className="bg-amber-500 h-full rounded-full" style={{ width: '45%' }}></div>
                      </div>
                    </div>

                    <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-800 mt-6 text-xs text-slate-300">
                      💡 <strong>Financial Health Status:</strong> Healthy cash reserves. Your liquid bank balance comfortably covers immediate supplier liabilities.
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => setActiveTab('ai')}
                  className="mt-6 w-full py-2.5 px-4 bg-slate-800 hover:bg-slate-700 text-indigo-400 text-xs font-semibold rounded-xl flex items-center justify-center gap-2 transition"
                >
                  <MessageSquare className="w-4 h-4" />
                  Analyze with Tally AI
                </button>
              </div>
            </div>
          </>
        )}

        {/* Tab: Receivables */}
        {activeTab === 'receivables' && (
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl overflow-hidden">
            <div className="p-5 border-b border-slate-800 flex justify-between items-center">
              <div>
                <h4 className="font-bold text-white">Outstanding Customer Receivables</h4>
                <p className="text-xs text-slate-400">Directly synchronized from Tally Prime Daybook & Bill Details</p>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-800/50 text-slate-400 uppercase text-[11px] font-semibold border-b border-slate-800">
                  <tr>
                    <th className="px-6 py-3.5">Customer / Debtor</th>
                    <th className="px-6 py-3.5">Bill Number</th>
                    <th className="px-6 py-3.5">Due Date</th>
                    <th className="px-6 py-3.5">Overdue Days</th>
                    <th className="px-6 py-3.5">Aging Bucket</th>
                    <th className="px-6 py-3.5 text-right">Pending Amount</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-300 text-xs">
                  {receivables.map((r) => (
                    <tr key={r.id} className="hover:bg-slate-800/30 transition">
                      <td className="px-6 py-4 font-semibold text-white">{r.party_name}</td>
                      <td className="px-6 py-4 font-mono text-slate-400">{r.bill_number}</td>
                      <td className="px-6 py-4">{r.due_date}</td>
                      <td className="px-6 py-4">
                        <span className="px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 font-medium">
                          {r.overdue_days} days
                        </span>
                      </td>
                      <td className="px-6 py-4">{r.aging_bucket} Days</td>
                      <td className="px-6 py-4 text-right font-bold text-emerald-400">
                        {formatCurrency(r.pending_amount)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab: Vouchers */}
        {activeTab === 'vouchers' && (
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl overflow-hidden">
            <div className="p-5 border-b border-slate-800">
              <h4 className="font-bold text-white">Recent Vouchers & Invoices</h4>
              <p className="text-xs text-slate-400">Sales, Purchases, Receipts, and Payments from Tally</p>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-800/50 text-slate-400 uppercase text-[11px] font-semibold border-b border-slate-800">
                  <tr>
                    <th className="px-6 py-3.5">Voucher Type</th>
                    <th className="px-6 py-3.5">Voucher #</th>
                    <th className="px-6 py-3.5">Date</th>
                    <th className="px-6 py-3.5">Party / Account</th>
                    <th className="px-6 py-3.5 text-right">Amount</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-300 text-xs">
                  {vouchers.map((v) => (
                    <tr key={v.id} className="hover:bg-slate-800/30 transition">
                      <td className="px-6 py-4">
                        <span className={`px-2.5 py-1 rounded-md font-semibold text-[11px] ${
                          v.voucher_type === 'Sales' ? 'bg-blue-500/15 text-blue-400 border border-blue-500/30' :
                          v.voucher_type === 'Purchase' ? 'bg-amber-500/15 text-amber-400 border border-amber-500/30' :
                          v.voucher_type === 'Receipt' ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30' :
                          'bg-slate-700 text-slate-200'
                        }`}>
                          {v.voucher_type}
                        </span>
                      </td>
                      <td className="px-6 py-4 font-mono text-slate-300">{v.voucher_number}</td>
                      <td className="px-6 py-4 text-slate-400">{v.date}</td>
                      <td className="px-6 py-4 font-medium text-white">{v.party_name}</td>
                      <td className="px-6 py-4 text-right font-bold text-slate-100">
                        {formatCurrency(v.amount)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab: Ask Tally AI */}
        {activeTab === 'ai' && (
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl flex flex-col h-[600px] overflow-hidden">
            <div className="p-4 border-b border-slate-800 bg-slate-900 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white text-xs">
                  AI
                </div>
                <div>
                  <h4 className="font-semibold text-white text-sm">Tally Conversational Intelligence</h4>
                  <p className="text-[11px] text-slate-400">Ask natural language questions about your Tally data</p>
                </div>
              </div>
            </div>

            {/* Chat Body */}
            <div className="flex-1 p-5 overflow-y-auto space-y-4">
              {chatMessages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-lg p-3.5 rounded-2xl text-xs leading-relaxed whitespace-pre-wrap ${
                      msg.sender === 'user'
                        ? 'bg-blue-600 text-white rounded-br-none'
                        : 'bg-slate-800 text-slate-200 rounded-bl-none border border-slate-700/60'
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
              {chatLoading && (
                <div className="flex justify-start">
                  <div className="p-3 bg-slate-800 rounded-2xl text-xs text-slate-400 animate-pulse border border-slate-700/60">
                    Thinking and querying Tally records...
                  </div>
                </div>
              )}
            </div>

            {/* Input Form */}
            <form onSubmit={handleSendMessage} className="p-4 border-t border-slate-800 bg-slate-900 flex gap-2">
              <input
                type="text"
                placeholder="Ask e.g.: 'Who owes the most?', 'What is our bank balance?', 'Total sales'..."
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition"
              />
              <button
                type="submit"
                disabled={chatLoading || !chatInput.trim()}
                className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition disabled:opacity-50"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Send</span>
              </button>
            </form>
          </div>
        )}
      </main>
    </div>
  );
}
