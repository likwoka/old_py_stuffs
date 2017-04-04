using System;
using RBFG.Insurance.Framework.DataParsing.Base;


namespace RBFG.Insurance.YJT0.DataParsing
{
	public class WQ222Response : Tran
	{

		public WQ222Response()
		{
			Segments.Add("WQ222Header", new WQ222Header());
			Segments.Add("ActivationStatusResponseList", new ActivationStatusResponseList());
			Segments.Add("MessageEndSegment", new MessageEndSegment());
		}


		public static WQ222Response ToObject(IState state)
		{		
			WQ222Response tran = new WQ222Response();
			WQ222Response result = new WQ222Response();

			int max = tran.Segments.Count;
			for (int i = 0; i < max; i++)
			{
				state = (tran.Segments[i]).ToObject(state);
				result.Segments[i] = state.Output as ISegment;
			}
			
			return result;
		}


		public WQ222Header WQ222Header
		{
			get
			{
				return Segments["WQ222Header"] as WQ222Header;
			}
			set
			{
				WQ222Header = value;
			}
		}

		
		public ActivationStatusResponseList ActivationStatusResponseList
		{
			get
			{
				return Segments["ActivationStatusResponseList"] as ActivationStatusResponseList;
			}

			set
			{
				ActivationStatusResponseList = value;
			}
		}		

		
		public MessageEndSegment MessageEndSegment
		{
			get
			{
				return Segments["MessageEndSegment"] as MessageEndSegment;
			}
			set
			{
				MessageEndSegment = value;
			}
		}
	}
}