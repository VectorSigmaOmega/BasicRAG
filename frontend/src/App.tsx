import React, { useState, useEffect, useRef } from 'react';
import { Settings, Upload, Send, Bot, User, Database, ChevronDown, ChevronRight, FileText } from 'lucide-react';
import './App.css';

interface Message {
  role: 'user' | 'bot';
  content: string;
  sources?: string[];
}

function App() {
  const [apiKey, setApiKey] = useState<string>('');
  const [query, setQuery] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [isQuerying, setIsQuerying] = useState<boolean>(false);
  const [uploadStatus, setUploadStatus] = useState<{ type: 'success' | 'error', text: string } | null>(null);
  const [uploadedFiles, setUploadedFiles] = useState<{name: string, chunks: number}[]>([]);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const API_BASE_URL = 'http://localhost:8000/api';

  useEffect(() => {
    const savedKey = localStorage.getItem('gemini_api_key');
    if (savedKey) setApiKey(savedKey);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleApiKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setApiKey(val);
    localStorage.setItem('gemini_api_key', val);
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;
    if (!apiKey) {
      setUploadStatus({ type: 'error', text: 'Please configure your API key first.' });
      return;
    }

    setIsUploading(true);
    setUploadStatus(null);
    
    let totalChunks = 0;
    let errors: string[] = [];

    for (const file of files) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
          method: 'POST',
          headers: {
            'x-api-key': apiKey
          },
          body: formData,
        });

        let data;
        let errorText = '';
        try {
          data = await response.json();
        } catch (e) {
          errorText = await response.text();
        }

        if (!response.ok) {
           throw new Error(data?.detail || errorText || `Upload failed with status: ${response.status} ${response.statusText}`);
        }
        
        totalChunks += data.chunks_count;
        setUploadedFiles(prev => [...prev, { name: data.filename, chunks: data.chunks_count }]);
      } catch (err: any) {
        console.error('Upload error:', err);
        errors.push(`${file.name}: ${err.message}`);
      }
    }

    setIsUploading(false);
    if (fileInputRef.current) fileInputRef.current.value = '';

    if (errors.length > 0) {
      setUploadStatus({ type: 'error', text: `Errors: ${errors.join(', ')}` });
    } else {
      setUploadStatus({ type: 'success', text: `Indexed ${files.length} file(s) successfully.` });
    }
  };

  const handleQuery = async () => {
    if (!query.trim() || !apiKey) return;

    const userMessage: Message = { role: 'user', content: query };
    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setIsQuerying(true);

    try {
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey
        },
        body: JSON.stringify({ query: userMessage.content }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Query failed');

      setMessages(prev => [...prev, { 
        role: 'bot', 
        content: data.answer,
        sources: data.context_chunks 
      }]);
    } catch (err: any) {
      setMessages(prev => [...prev, { role: 'bot', content: `Error: ${err.message}` }]);
    } finally {
      setIsQuerying(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleQuery();
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar Configuration */}
      <aside className="sidebar">
        <div className="brand">
          <Database size={24} />
          <span>Knowledge Base</span>
        </div>

        <div className="api-key-section">
          <h3 className="section-title">Configuration</h3>
          <div style={{ position: 'relative' }}>
            <Settings size={16} style={{ position: 'absolute', top: 11, left: 10, color: 'var(--text-secondary)' }} />
            <input 
              type="password" 
              placeholder="Google Gemini API Key" 
              value={apiKey}
              onChange={handleApiKeyChange}
              className="input-field"
              style={{ paddingLeft: '2rem' }}
            />
          </div>
          <small style={{ color: 'var(--text-secondary)', fontSize: '0.75rem' }}>
            Stored securely in your browser's local storage.
          </small>
        </div>

        <div className="upload-section">
          <h3 className="section-title">Documents</h3>
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileUpload} 
            className="file-input" 
            accept=".pdf,.txt"
            multiple
          />
          <button 
            className="btn btn-outline" 
            onClick={() => fileInputRef.current?.click()}
            disabled={isUploading || !apiKey}
          >
            {isUploading ? 'Processing...' : <><Upload size={18} /> Upload Document(s)</>}
          </button>
          {uploadStatus && (
            <div className={`status-message status-${uploadStatus.type}`}>
              {uploadStatus.text}
            </div>
          )}
          
          {uploadedFiles.length > 0 && (
            <div style={{ marginTop: '1rem' }}>
              <h4 style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Indexed Documents</h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {uploadedFiles.map((f, i) => (
                  <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', padding: '0.5rem', backgroundColor: 'var(--bg-color)', borderRadius: 'var(--radius-md)' }}>
                    <FileText size={14} color="var(--primary-color)" style={{ flexShrink: 0 }} />
                    <span style={{ flex: 1, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }} title={f.name}>{f.name}</span>
                    <span style={{ color: 'var(--text-secondary)', flexShrink: 0 }}>{f.chunks} chunks</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </aside>

      {/* Main Chat Interface */}
      <main className="main-area">
        <div className="chat-history">
          {messages.length === 0 ? (
            <div className="empty-state">
              <Bot size={48} />
              <h2>Welcome to your Knowledge Base</h2>
              <p>Upload a document and start asking questions.</p>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className="message">
                <div className={`message-icon ${msg.role === 'user' ? 'user-icon' : 'bot-icon'}`}>
                  {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                </div>
                <div className="message-content">
                  <p>{msg.content}</p>
                  {msg.sources && msg.sources.length > 0 && (
                    <SourceAccordion sources={msg.sources} />
                  )}
                </div>
              </div>
            ))
          )}
          {isQuerying && (
             <div className="message">
               <div className="message-icon bot-icon"><Bot size={20} /></div>
               <div className="message-content"><p>Thinking...</p></div>
             </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <div className="chat-input-area">
          <div className="input-wrapper">
            <input 
              type="text" 
              className="chat-input"
              placeholder="Ask a question about your documents..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isQuerying || !apiKey}
            />
            <button 
              className="send-btn" 
              onClick={handleQuery}
              disabled={!query.trim() || isQuerying || !apiKey}
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

const SourceAccordion = ({ sources }: { sources: string[] }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="sources">
      <button className="source-toggle" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? <ChevronDown size={14} style={{display:'inline', verticalAlign:'middle'}}/> : <ChevronRight size={14} style={{display:'inline', verticalAlign:'middle'}}/>}
        {isOpen ? ' Hide Sources' : ' Show Sources'}
      </button>
      {isOpen && (
        <div className="sources-list">
          {sources.map((src, idx) => (
            <div key={idx} className="source-item">
              <FileText size={14} style={{display:'inline', verticalAlign:'middle', marginRight: 4, color:'var(--text-secondary)'}} />
              <span style={{ fontSize: '0.8rem' }}>{src.substring(0, 150)}...</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default App;
