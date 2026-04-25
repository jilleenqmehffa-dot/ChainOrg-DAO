import React from 'react';
import UserRegistration from './components/UserRegistration';

function App() {
  return (
    <div className="App">
      <header>
        <h1>ChainOrg-DAO 平台</h1>
        <p>基于模拟区块链的去中心化自治组织系统</p>
      </header>
      
      <main>
        <section>
          <UserRegistration />
        </section>
      </main>
    </div>
  );
}

export default App;