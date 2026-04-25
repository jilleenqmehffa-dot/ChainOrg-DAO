// API 服务层 - ChainOrg-DAO 前端与后端通信

// API基础URL - 您的后端API运行在这个地址
const API_BASE_URL = 'http://localhost:8000/api/v1';

// 用户相关的API请求
export const userAPI = {
  // 创建新用户
  createUser: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/users/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      throw new Error(`创建用户失败: ${response.status}`);
    }

    return response.json();
  },

  // 获取用户详情
  getUserById: async (userId) => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`);

    if (!response.ok) {
      throw new Error(`获取用户失败: ${response.status}`);
    }

    return response.json();
  },

  // 根据地址获取用户
  getUserByAddress: async (address) => {
    const response = await fetch(`${API_BASE_URL}/users/address/${address}`);

    if (!response.ok) {
      throw new Error(`获取用户失败: ${response.status}`);
    }

    return response.json();
  },
  
  // 获取所有用户 - 但后端似乎没有这个接口
  // 我们只添加后端实际支持的功能
};

// 提案相关的API请求
export const proposalAPI = {
  // 创建提案
  createProposal: async (proposalData) => {
    const response = await fetch(`${API_BASE_URL}/proposals/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(proposalData),
    });

    if (!response.ok) {
      throw new Error(`创建提案失败: ${response.status}`);
    }

    return response.json();
  },

  // 获取所有提案
  getAllProposals: async () => {
    const response = await fetch(`${API_BASE_URL}/proposals/`);

    if (!response.ok) {
      throw new Error(`获取提案失败: ${response.status}`);
    }

    return response.json();
  },

  // 获取特定提案
  getProposalById: async (proposalId) => {
    const response = await fetch(`${API_BASE_URL}/proposals/${proposalId}`);

    if (!response.ok) {
      throw new Error(`获取提案失败: ${response.status}`);
    }

    return response.json();
  }
};

// 投票相关的API请求
export const voteAPI = {
  // 创建投票
  createVote: async (voteData) => {
    const response = await fetch(`${API_BASE_URL}/votes/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(voteData),
    });

    if (!response.ok) {
      throw new Error(`投票失败: ${response.status}`);
    }

    return response.json();
  }
};