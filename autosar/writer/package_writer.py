from autosar.writer.writer_base import WriterBase
from autosar.writer.datatype_writer import DataTypeWriter
from autosar.writer.constant_writer import ConstantWriter
from autosar.writer.component_writer import ComponentTypeWriter
from autosar.writer.behavior_writer import BehaviorWriter
from autosar.writer.portinterface_writer import PortInterfaceWriter


class PackageWriter(WriterBase):
   def __init__(self,version):
      super().__init__(version)
      self.dataTypeWriter = DataTypeWriter(version)
      self.constantWriter = ConstantWriter(version)
      self.componentTypeWriter = ComponentTypeWriter(version)
      self.behaviorWriter = BehaviorWriter(version)
      self.portInterfaceWriter = PortInterfaceWriter(version)
      if self.version >= 3.0:
         self.switcherXML = {'ArrayDataType': self.dataTypeWriter.writeArrayDataTypeXml,
                          'BooleanDataType': self.dataTypeWriter.writeBooleanDataTypeXml,
                          'IntegerDataType': self.dataTypeWriter.writeIntegerTypeXML,
                          'RealDataType': self.dataTypeWriter.writeRealDataTypeXML,
                          'RecordDataType': self.dataTypeWriter.writeRecordDataTypeXML,
                          'StringDataType': self.dataTypeWriter.writeStringTypeXml,
                          'ApplicationSoftwareComponent': self.componentTypeWriter.writeApplicationSoftwareComponentXML,
                          'COMPLEX-DEVICE-DRIVER-COMPONENT-TYPE': None,
                          'InternalBehavior': self.behaviorWriter.writeInternalBehaviorXML,
                          'SwcImplementation': self.componentTypeWriter.writeSwcImplementationXML,
                          'CompuMethodConst': self.dataTypeWriter.writeCompuMethodXML,
                          'CompuMethodRational': self.dataTypeWriter.writeCompuMethodXML,
                          'DataTypeUnitElement': self.dataTypeWriter.writeDataTypeUnitElementXML,
                          'SoftwareAddressMethod': self.portInterfaceWriter.writeSoftwareAddressMethodXML,
                          'ModeDeclarationGroup': self.portInterfaceWriter.writeModeDeclarationGroupXML,
                          'SenderReceiverInterface': self.portInterfaceWriter.writeSenderReceiverInterfaceXML,
                          'ParameterInterface': self.portInterfaceWriter.writeParameterInterfaceXML,
                          'ClientServerInterface': self.portInterfaceWriter.writeClientServerInterfaceXML,
                          'Constant': self.constantWriter.writeConstantXML,
                          'COMPOSITION-TYPE': None,
                          'SYSTEM-SIGNAL': None,
                          'SYSTEM': None
                          }
         self.switcherCode = {'ArrayDataType': self.dataTypeWriter.writeArrayDataTypeCode,
                          'BooleanDataType': self.dataTypeWriter.writeBooleanDataTypeCode,
                          'IntegerDataType': self.dataTypeWriter.writeIntegerTypeCode,
                          'RealDataType': self.dataTypeWriter.writeRealDataTypeCode,
                          'RecordDataType': self.dataTypeWriter.writeRecordDataTypeCode,
                          'StringDataType': self.dataTypeWriter.writeStringTypeCode,
                          'ApplicationSoftwareComponent': self.componentTypeWriter.writeApplicationSoftwareComponentCode,
                          'COMPLEX-DEVICE-DRIVER-COMPONENT-TYPE': None,
                          'InternalBehavior': self.behaviorWriter.writeInternalBehaviorCode,
                          'SwcImplementation': self.componentTypeWriter.writeSwcImplementationCode,
                          'CompuMethodConst': self.dataTypeWriter.writeCompuMethodCode,
                          'CompuMethodRational': self.dataTypeWriter.writeCompuMethodCode,
                          'DataTypeUnitElement': self.dataTypeWriter.writeDataTypeUnitElementCode,
                          'SoftwareAddressMethod': self.portInterfaceWriter.writeSoftwareAddressMethodCode,
                          'ModeDeclarationGroup': self.portInterfaceWriter.writeModeDeclarationGroupCode,
                          'SenderReceiverInterface': self.portInterfaceWriter.writeSenderReceiverInterfaceCode,
                          'ParameterInterface': self.portInterfaceWriter.writeParameterInterfaceCode,
                          'ClientServerInterface': self.portInterfaceWriter.writeClientServerInterfaceCode,
                          'Constant': self.constantWriter.writeConstantCode,
                          'COMPOSITION-TYPE': None,
                          'SYSTEM-SIGNAL': None,
                          'SYSTEM': None
                          }
      else:
         raise NotImplementedError("AUTOSAR version not yet supported")
   
   def toXML(self,package):      
      lines=[]
      lines.extend(self.beginPackage(package.name))
      if len(package.elements)>0:
         lines.append(self.indent("<ELEMENTS>",1))
         for elem in package.elements:
            writerFunc = self.switcherXML.get(elem.__class__.__name__)
            if writerFunc is not None:            
               lines.extend(self.indent(writerFunc(elem,package),2))
            else:
               print("skipped: %s"%str(type(elem)))
         lines.append(self.indent("</ELEMENTS>",1))
      else:
         lines.append(self.indent("<ELEMENTS/>",1))
      if len(package.subPackages)>0:
         lines.append(self.indent("<SUB-PACKAGES>",1))
         for subPackage in package.subPackages:
            lines.extend(self.indent(self.toXML(subPackage),2))
         lines.append(self.indent("</SUB-PACKAGES>",1))
      lines.extend(self.endPackage())
      return lines
   
   def toCode(self, package, localvars):
      lines=[]
      if package.role is not None:
         lines.append('package=ws.createPackage("%s", role="%s")'%(package.name, package.role))
      else:
         lines.append('package=ws.createPackage("%s")'%(package.name))
      localvars['package']=package
      for subPackage in package.subPackages:
         if subPackage.role is not None:
            lines.append('package.createSubPackage("%s", role="%s")'%(subPackage.name, subPackage.role))
         else:
            lines.append('package.createSubPackage("%s")'%(subPackage.name))            
      for elem in package.elements:
         writerFunc = self.switcherCode.get(elem.__class__.__name__)
         if writerFunc is not None:
            lines.extend(writerFunc(elem, localvars))
         else:
            raise NotImplementedError(type(elem))            
      return lines