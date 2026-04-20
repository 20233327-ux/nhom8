import { ChevronDown, ChevronRight, Plus } from 'lucide-react';
import { useState } from 'react';

interface MenuItem {
  label: string;
  addAction?: string;
  changeAction?: string;
}

interface MenuSection {
  title: string;
  items: MenuItem[];
  isExpanded?: boolean;
}

export default function App() {
  const [sections, setSections] = useState<MenuSection[]>([
    {
      title: 'VN_DOCS',
      isExpanded: true,
      items: [
        { label: 'Danh sách Công văn', addAction: 'Thêm vào', changeAction: 'Thay đổi' }
      ]
    },
    {
      title: 'VN_USERS',
      isExpanded: true,
      items: [
        { label: 'Người dùng', addAction: 'Thêm vào', changeAction: 'Thay đổi' },
        { label: 'Phòng ban', addAction: 'Thêm vào', changeAction: 'Thay đổi' }
      ]
    },
    {
      title: 'VN_WORKFLOW',
      isExpanded: true,
      items: [
        { label: 'Approval historys', addAction: 'Thêm vào', changeAction: 'Thay đổi' },
        { label: 'Các quy trình duyệt', addAction: 'Thêm vào', changeAction: 'Thay đổi' },
        { label: 'Document workflows', addAction: 'Thêm vào', changeAction: 'Thay đổi' }
      ]
    },
    {
      title: 'XÁC THỰC VÀ ỦY QUYỀN',
      isExpanded: true,
      items: [
        { label: 'Các nhóm', addAction: 'Thêm vào', changeAction: 'Thay đổi' }
      ]
    }
  ]);

  const toggleSection = (index: number) => {
    setSections(sections.map((section, i) => 
      i === index ? { ...section, isExpanded: !section.isExpanded } : section
    ));
  };

  const recentActivities = [
    {
      id: '1',
      action: '1231231 - biết gì không',
      user: 'công văn',
      type: 'edit'
    },
    {
      id: '2', 
      action: 'duy123',
      user: 'Người dùng',
      type: 'edit'
    },
    {
      id: '3',
      action: 'ký thuật',
      user: 'Phòng ban',
      type: 'add'
    }
  ];

  return (
    <div className="size-full bg-[#1a1a1a] text-white overflow-hidden">
      {/* Header */}
      <header className="bg-[#4a7c99] px-6 py-3 flex items-center justify-between">
        <h1 className="text-xl">Trang quản trị cho Django</h1>
        <nav className="flex items-center gap-4 text-sm">
          <span>CHÀO MỪNG BẠN, <strong>ADMIN</strong></span>
          <a href="#" className="hover:underline">XEM TRANG WEB</a>
          <span>/</span>
          <a href="#" className="hover:underline">ĐỔI MẬT KHẨU</a>
          <span>/</span>
          <a href="#" className="hover:underline">THOÁT</a>
        </nav>
      </header>

      <div className="flex h-[calc(100%-60px)]">
        {/* Sidebar */}
        <aside className="w-[450px] bg-[#2b2b2b] p-4 overflow-y-auto border-r border-[#3a3a3a]">
          <h2 className="text-lg mb-4">Site quản trị hệ thống.</h2>
          
          <div className="space-y-2">
            {sections.map((section, sectionIndex) => (
              <div key={sectionIndex} className="mb-2">
                <button
                  onClick={() => toggleSection(sectionIndex)}
                  className="w-full bg-[#4a7c99] px-4 py-2 text-left flex items-center justify-between hover:bg-[#5a8ca9] transition-colors"
                >
                  <span className="uppercase text-sm font-medium">{section.title}</span>
                  {section.isExpanded ? (
                    <ChevronDown className="w-4 h-4" />
                  ) : (
                    <ChevronRight className="w-4 h-4" />
                  )}
                </button>
                
                {section.isExpanded && (
                  <div className="bg-[#1f1f1f] border-l-2 border-[#4a7c99]">
                    {section.items.map((item, itemIndex) => (
                      <div
                        key={itemIndex}
                        className="flex items-center justify-between px-4 py-3 hover:bg-[#2a2a2a] border-b border-[#2b2b2b]"
                      >
                        <span className="text-sm text-gray-200">{item.label}</span>
                        <div className="flex items-center gap-2">
                          {item.addAction && (
                            <button className="text-[#6ac174] text-xs flex items-center gap-1 hover:text-[#7ad184]">
                              <Plus className="w-3 h-3" />
                              {item.addAction}
                            </button>
                          )}
                          {item.changeAction && (
                            <button className="text-[#6ac174] text-xs flex items-center gap-1 hover:text-[#7ad184]">
                              <svg className="w-3 h-3" viewBox="0 0 16 16" fill="currentColor">
                                <path d="M13.5 1.5l1 1-10 10H3.5v-1l10-10zm1.707-.707a1 1 0 0 0-1.414 0l-10 10A1 1 0 0 0 3.5 11.5v1a1 1 0 0 0 1 1h1a1 1 0 0 0 .707-.293l10-10a1 1 0 0 0 0-1.414l-1-1z"/>
                              </svg>
                              {item.changeAction}
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6 overflow-y-auto">
          <div className="space-y-8">
            {/* Recent Activity */}
            <section>
              <h2 className="text-xl mb-4">Hoạt động gần đây</h2>
            </section>

            {/* My Activity */}
            <section>
              <h2 className="text-xl mb-4">Hoạt động của tôi</h2>
              
              <div className="space-y-2">
                {recentActivities.map((activity) => (
                  <div key={activity.id} className="text-sm">
                    <div className="flex items-start gap-2">
                      <span className="text-[#6ac174]">+</span>
                      <div>
                        <a href="#" className="text-[#6ac174] hover:underline">
                          {activity.action}
                        </a>
                        <div className="text-gray-400 text-xs mt-1">
                          {activity.user}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}
