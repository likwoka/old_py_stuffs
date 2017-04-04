using System;
using RBFG.Insurance.Framework.DataParsing.Base;


namespace RBFG.Insurance.YJT0.DataParsing
{
	public class MessageEndSegment : Segment
	{

		public MessageEndSegment()
		{
			Fields.Add("Label", new Field(FT.Alpha, 6, "@@ENDM"));
			Fields.Add("EndSegment", new Field(FT.Alpha, 1, "|"));
		}


		public string Label
		{
			get
			{
				return Fields["Label"].String;
			}
			set
			{
				Fields["Label"].String = value;
			}
		}


		public string EndSegment
		{
			get
			{
				return Fields["EndSegment"].String;
			}
			set
			{
				Fields["EndSegment"].String = value;
			}
		}
	}
}