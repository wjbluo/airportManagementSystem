// var SystemMenu = [{
// 	title: '系统管理',
// 	icon: '&#xe6ed;',
// 	isCurrent: true,
// 	menu: [{
// 		title: '供应商管理',
// 		icon: '&#xe620;',
// 		isCurrent: true,
// 		children: [{
// 			title: '首页',
// 			href: 'workbench.html',
// 			isCurrent: true
// 		},{
// 			title: '二级页面',
// 			children: [{
// 				title: '三级页面1',
// 				href: 'workbench.html'
// 			},{
// 				title: '三级页面2',
// 				href: 'basic_info.html'
// 			},{
// 				title: '三级页面3',
// 				href: 'workbench.html'
// 			},{
// 				title: '三级页面4',
// 				href: 'basic_info.html'
// 			},{
// 				title: '三级页面5',
// 				href: 'workbench.html'
// 			}]
// 		},{
// 			title: '招标流程',
// 			href: 'process.html'
// 		},{
// 			title: '供应商列表',
// 			href: 'providers.html'
// 		},{
// 			title: '详细信息',
// 			href: 'providers1.html'
// 		},{
// 			title: '企业基本信息',
// 			href: 'basic_info.html'
// 		}]
// 	},{
// 		title: '采购组织',
// 		icon: '&#xe625;',
// 		href: 'basic_info.html',
// 		children: []
// 	},{
// 		title: '专家库',
// 		icon: '&#xe62f;',
// 		children: [{
// 			title: '专家管理',
// 			href: 'providers.html'
// 		},{
// 			title: '添加专家',
// 			href: 'providers1.html'
// 		},{
// 			title: '审核专家',
// 			href: 'basic_info.html'
// 		}]
// 	},{
// 		title: '注册供应商',
// 		icon: '&#xe647;',
// 		children: [{
// 			title: '供应商管理',
// 			href: 'providers.html'
// 		},{
// 			title: '进货渠道',
// 			href: 'providers1.html'
// 		},{
// 			title: '自定义',
// 			href: 'basic_info.html'
// 		}]
// 	},{
// 		title: 'RFI动态信息',
// 		icon: '&#xe611;',
// 		href: 'providers.html',
// 		children: []
// 	},{
// 		title: '权限模块',
// 		icon: '&#xe6fd;',
// 		children: [{
// 			title: '角色管理',
// 			href: 'sysManage/authorization/roleManag/'
// 		}, {
//             title: '员工管理',
//             href: 'sysManage/authorization/userManag/'
//         }]
// 	}]
// },{
// 	title: '道面管理',
// 	icon: '&#xe6a6;',
// 	menu: [{
// 		title: '信息控制台',
// 		icon: '&#xe6f0;',
// 		isCurrent: true,
// 		children: [{
// 			title: '道面日常维护管理',
// 			href: 'pavementManage/workbench.html',
// 			isCurrent: true
// 		},{
// 			title: '跑滑及滑行道日常巡视',
// 			children: [{
// 				title: '查看异常附件',
// 				href: 'workbench.html'
// 			},{
// 				title: '新增跑滑巡视日志',
// 				href: 'basic_info.html'
// 			},{
// 				title: '新增跑滑异常日志',
// 				href: 'workbench.html'
// 			},{
// 				title: '异常记录选择',
// 				href: 'basic_info.html'
// 			},{
// 				title: '巡视台账输出日志',
// 				href: 'workbench.html'
// 			},{
// 				title: '巡视台账输出异常',
// 				href: 'workbench.html'
// 			}]
// 		},{
// 			title: '机坪及附属设施日常巡视',
// 			children: [{
// 				title: '异常查看',
// 				href: 'workbench.html'
// 			},{
// 				title: '新增机坪巡视日志',
// 				href: 'basic_info.html'
// 			},{
// 				title: '新增机坪异常记录',
// 				href: 'workbench.html'
// 			},{
// 				title: '机坪巡视电子台账日志',
// 				href: 'workbench.html'
// 			},{
// 				title: '机坪巡视电子台账病害',
// 				href: 'workbench.html'
// 			}]
// 		},{
// 			title: '场道异常情况报告',
// 			children: [{
// 				title: '异常报告',
// 				href: 'workbench.html'
// 			},{
// 				title: '应急维修',
// 				href: 'basic_info.html'
// 			},{
// 				title: '尽快维修',
// 				href: 'workbench.html'
// 			},{
// 				title: '近期维修',
// 				href: 'workbench.html'
// 			},{
// 				title: '跟踪关注',
// 				href: 'workbench.html'
// 			},{
// 				title: '异常记录详情',
// 				href: 'workbench.html'
// 			},{
// 				title: '完成情况查看',
// 				href: 'workbench.html'
// 			},{
// 				title: '异常附件查看',
// 				href: 'workbench.html'
// 			}]
// 		}]
// 	},{
// 		title: '附属设施维护管理',
// 		icon: '&#xe611;',
// 		children: [{
// 			title: '飞行区附属设施异常报告',
// 			href: 'process.html'
// 		},{
// 			title: '道面清扫保洁及FOD',
// 			children: [{
// 				title: '新增清扫保洁记录',
// 				href: 'workbench.html'
// 			},{
// 				title: '添加外来物',
// 				href: 'basic_info.html'
// 			},{
// 				title: '道面FOD汇总',
// 				href: 'workbench.html'
// 			}]
// 		},{
// 			title: '跑道摩擦系数与涂胶',
// 			href: 'process.html'
// 		}]
// 	}]
// },{
// 	title: '灯光管理',
// 	icon: '&#xe653;',
// 	menu: [{
// 		title: '数据信息',
// 		icon: '&#xe647;',
// 		isCurrent: true,
// 		children: [{
// 			title: '数据管理',
// 			href: 'process.html',
// 			isCurrent: true
// 		},{
// 			title: '企业荣誉',
// 			href: 'index.html'
// 		},{
// 			title: '组织架构',
// 			href: 'index.html'
// 		},{
// 			title: '自定义',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '数据表',
// 		icon: '&#xe611;',
// 		href: 'basic_info.html',
// 		children: []
// 	}]
// },{
// 	title: '合同管理',
// 	icon: '&#xe64c;',
// 	menu: [{
// 		title: '合同归档',
// 		icon: '&#xe647;',
// 		isCurrent: true,
// 		children: [{
// 			title: '合同发布',
// 			href: 'basic_info.html',
// 			isCurrent: true
// 		},{
// 			title: '合同制度管理',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '合同信息',
// 		icon: '&#xe611;',
// 		href: 'basic_info.html',
// 		children: []
// 	}]
// },{
// 	title: '土面区管理',
// 	icon: '&#xe643;',
// 	menu: [{
// 		title: '合同归档',
// 		icon: '&#xe647;',
// 		isCurrent: true,
// 		children: [{
// 			title: '合同发布',
// 			href: 'index.html',
// 			isCurrent: true
// 		},{
// 			title: '合同制度管理',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '合同信息',
// 		icon: '&#xe611;',
// 		href: 'basic_info.html',
// 		children: []
// 	}]
// },{
// 	title: '自定义',
// 	icon: '&#xe646;',
// 	menu: [{
// 		title: '合同归档',
// 		icon: '&#xe647;',
// 		isCurrent: true,
// 		children: [{
// 			title: '合同发布',
// 			href: 'workbench.html',
// 			isCurrent: true
// 		},{
// 			title: '合同制度管理',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '合同信息',
// 		icon: '&#xe611;',
// 		href: 'basic_info.html',
// 		children: []
// 	}]
// },{
// 	title: '自定义',
// 	icon: '&#xe646;',
// 	menu: [{
// 		title: '合同归档',
// 		icon: '&#xe647;',
// 		isCurrent: true,
// 		children: [{
// 			title: '合同发布',
// 			href: 'basic_info.html',
// 			isCurrent: true
// 		},{
// 			title: '合同制度管理',
// 			href: 'index.html'
// 		}]
// 	},{
// 		title: '合同信息',
// 		icon: '&#xe611;',
// 		href: 'basic_info.html',
// 		children: []
// 	}]
// }];