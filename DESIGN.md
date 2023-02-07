# 整体框架设计

与之前的智齐网站做对比：
* 智齐的数据库模型：
    * User 用户：员工、医生、管理员
    * Staff 公司员工、主要处理操作权限问题：目前的话有管理员、资料审核员、数据分割融合准备员、排牙员、数据分割融合审核员、排牙员、排牙审核员、生产车间
    * Doctor 医生
    * Patient 病人
    * STLCommonFiles 数据融合员的输出
    * PhotoName 患者照片名称
    * PatientPhoto 患者照片
    * Message 留言
    * HandleData 处理患者数据中间表，针对于数据分割融合员
    * ProduceProduct 生产车间生产患者产品
    * Arrange 排牙
    * CheckResult 审核人员中间表
    * CheckArrange 排牙人员审核排牙方案
    * MaterialCheck 资料审核员审核医生提交的患者资料
    * Settings 全局设置，主要是审核率
    * BackMessage 资料不合格返回信息
    * DiagnosisDesign 诊断设计表，和患者是一对多的关系
    * DiagnosisModifyLog 患者方案修改日志
    * FirstLevelLabel、SecondLevelLabel、PatientLabel 病例标签
    * ArrangeAdvice 排牙员和排牙审核员的沟通
    * EmailMessage 邮件存储
    * WithdrawRecords 记录管理员撤回的病例
    有一些已经没用了，比如add_tag