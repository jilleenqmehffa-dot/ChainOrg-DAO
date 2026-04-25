// 用户注册组件
import React, { useState } from 'react';
import { userAPI } from '../services/api';

const UserRegistration = () => {
  // 用于存储表单数据的状态
  const [username, setUsername] = useState('');
  // 用于显示错误信息的状态
  const [error, setError] = useState('');

  // 处理表单提交事件
  const handleSubmit = async (e) => {
    e.preventDefault(); // 阻止表单默认提交行为
    
    try {
      // 调用API创建新用户
      const newUser = await userAPI.createUser({
        username: username
      });
      
      // 成功注册后，在控制台输出结果
      console.log('用户注册成功:', newUser);
      alert(`用户创建成功，钱包地址: ${newUser.mock_address}`);
      
      // 清空输入框
      setUsername('');
    } catch (err) {
      // 如果出现错误，显示错误信息
      setError(err.message);
      console.error('注册失败:', err);
    }
  };

  return (
    <div>
      <h2>用户注册</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>用户名：</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="输入用户名"
            required
          />
        </div>
        <button type="submit">注册</button>
      </form>
      {error && <p style={{color: 'red'}}>错误: {error}</p>}
    </div>
  );
};

export default UserRegistration;